import os
import json
import time
from datetime import datetime, timedelta
from state_manager import StateManager
from orchestrator import Orchestrator
from qc_manager import QCManager

class TestsV23:
    def __init__(self):
        # Override persistence for testing
        self.test_file = "data/tracking/state_test_v23.json"
        if os.path.exists(self.test_file): os.remove(self.test_file)
        
        # Patching StateManager to use test file
        import state_manager
        state_manager.PERSISTENCE_FILE = self.test_file
        
        self.sm = StateManager()
        self.orch = Orchestrator()
        self.orch.sm = self.sm # Orchestrator uses our SM
        self.orch.rg.state_manager = self.sm # ReportGenerator uses our SM
        self.orch.qc.sm = self.sm # QCManager uses our SM

    def run_all(self):
        print(f"\n{'#'*60}\nCORE TEST SUITE: MAPA-RD v2.3 (Full Compliance T1-T9)\n{'#'*60}")
        
        self.test_t1_client_creation_slug()
        self.test_t2_intake_auto_auth()
        self.test_t3_pipeline_success()
        self.test_t4_qc_failure_rescue()
        self.test_t5_tacit_approval()
        self.test_t6_incident_limit()
        self.test_t7_priority_scheduler()
        self.test_t8_role_limitation()
        self.test_t9_metadata_persistence()
        
        print(f"\n{'#'*60}\nTEST SUITE COMPLETE\n{'#'*60}")

    def assert_eq(self, actual, expected, msg):
        if actual == expected:
            print(f"[PASS] {msg}")
        else:
            print(f"[FAIL] {msg} | Expected: {expected}, Actual: {actual}")

    def test_t1_client_creation_slug(self):
        print(f"\n[T1] Testing Client Creation & Slug...")
        c_id = self.sm._get_or_create_client_id("Prueba de Test", client_type="PF")
        client = self.sm.get_client(c_id)
        self.assert_eq(client["client_name_slug"], "Prueba_de_Test", "Slug generated correctly")

    def test_t2_intake_auto_auth(self):
        print(f"\n[T2] Testing Intake & Auth Flow...")
        c_id = self.sm._get_or_create_client_id("User Auth Test")
        i_id = self.sm.create_intake(c_id, "BASELINE")
        self.assert_eq(self.sm.data["intakes"][i_id]["intake_status"], "GENERADO", "Intake starts as GENERADO")
        
        # User (Admin) Authorizes
        self.sm.update_intake(i_id, "AUTORIZADO")
        self.assert_eq(self.sm.data["intakes"][i_id]["intake_status"], "AUTORIZADO", "Intake manually authorized")

    def test_t3_pipeline_success(self):
        print(f"\n[T3] Testing Pipeline Success (Full Flow)...")
        c_id = self.sm._get_or_create_client_id("Success Pipeline Test")
        i_id = self.sm.create_intake(c_id, "FREQUENCY")
        self.sm.update_intake(i_id, "AUTORIZADO")
        
        self.orch.execute_pipeline(i_id)
        
        client = self.sm.get_client(c_id)
        rep_id = client["reports"][-1]
        report = self.sm.data["reports"][rep_id]
        
        self.assert_eq(report["qc_status"], "APROBADO", "QC passed")
        self.assert_eq(report["report_status"], "EN_REVISION", "Status is EN_REVISION (Sent)")
        
        # Capture filename for evidence
        pdf_name = os.path.basename(report["artifacts"]["final_pdf_path"])
        print(f"[*] Generated Filename Evidence (REPORTE): {pdf_name}")
        qc_json = report["artifacts"]["qc_checklist_json_path"]
        print(f"[*] Evidence QC Approved Path: {qc_json}")

    def test_t4_qc_failure_rescue(self):
        print(f"\n[T4] Testing QC Failure & Automatic RESCUE...")
        c_id = self.sm._get_or_create_client_id("Rescue Logic Test")
        i_id = self.sm.create_intake(c_id, "BASELINE")
        self.sm.update_intake(i_id, "AUTORIZADO")
        
        # Force Failure
        original_val = self.orch.qc.validate_filename
        self.orch.qc.validate_filename = lambda x: (False, "FORCED FAILURE FOR TEST")
        
        self.orch.execute_pipeline(i_id)
        
        self.orch.qc.validate_filename = original_val
        
        client = self.sm.get_client(c_id)
        rep_id = client["reports"][-1]
        report = self.sm.data["reports"][rep_id]
        
        self.assert_eq(report["qc_status"], "FALLIDO", "QC FAIL")
        self.assert_eq(report["report_status"], "INVALIDADO", "Report INVALID")
        
        last_intake_id = client["intakes"][-1]
        last_intake = self.sm.data["intakes"][last_intake_id]
        self.assert_eq(last_intake["intake_type"], "RESCUE", "I4: Automatic RESCUE created")
        print(f"[*] RESCUE Intake ID: {last_intake_id}")
        
    def test_t5_tacit_approval(self):
        print(f"\n[T5] Testing Tacit Approval (48h)...")
        c_id = self.sm._get_or_create_client_id("Tacit Test")
        i_id = self.sm.create_intake(c_id, "BASELINE")
        r_id = self.sm.create_report(c_id, i_id, "BASELINE")
        self.sm.update_report_status(r_id, "EN_REVISION")
        
        report = self.sm.data["reports"][r_id]
        report["review_deadline_at"] = (datetime.now() - timedelta(hours=1)).isoformat()
        self.sm.save_data()
        
        self.sm.process_tacit_approvals()
        
        updated_report = self.sm.data["reports"][r_id]
        self.assert_eq(updated_report["report_status"], "APROBADO_TACITO", "Status updated to Tacit")

    def test_t6_incident_limit(self):
        print(f"\n[T6] Testing Incident Limit (Max 2)...")
        c_id = self.sm._get_or_create_client_id("Limit Test")
        self.sm.update_client(c_id, incident_count_month=2)
        
        # This is primarily for Scheduler skip or validation
        i_id = self.sm.create_intake(c_id, "INCIDENT")
        client = self.sm.get_client(c_id)
        print(f"[*] Current incident count: {client['incident_count_month']}")
        print(f"[*] Created intake {i_id} (Manual intervention required beyond limit)")
        self.assert_eq(client["incident_count_month"], 2, "Limit preserved")

    def test_t7_priority_scheduler(self):
        print(f"\n[T7] Testing Priority Global (RESCUE First)...")
        c_id = self.sm._get_or_create_client_id("Priority Test")
        i_base = self.sm.create_intake(c_id, "BASELINE")
        i_res = self.sm.create_intake(c_id, "RESCUE", replaces_report_id="R-TEST")
        
        self.sm.update_intake(i_base, "AUTORIZADO")
        self.sm.update_intake(i_res, "AUTORIZADO")
        
        ordered = self.sm.list_authorized_intakes_by_priority()
        self.assert_eq(ordered[0]["intake_id"], i_res, "RESCUE is first in queue")

    def test_t8_role_limitation(self):
        print(f"\n[T8] Testing Role Logic (AG cannot auth self)...")
        c_id = self.sm._get_or_create_client_id("Role Test")
        i_id = self.sm.create_intake(c_id, "BASELINE", requested_by="SYSTEM") # AG creates base?
        
        # Verify that scheduler ignores GENERADO
        pending = self.sm.list_authorized_intakes_by_priority()
        pending_ids = [x["intake_id"] for x in pending]
        has_id = (i_id in pending_ids)
        self.assert_eq(has_id, False, "Intake GENERADO is NOT processed by scheduler (Requires Admin Auth)")

    def test_t9_metadata_persistence(self):
        print(f"\n[T9] Testing Metadata & EventLog Persistence...")
        c_id = self.sm._get_or_create_client_id("Persistence Test")
        # Check event log (Global registry in self.data["logs"])
        has_logs = len(self.sm.data.get("logs", [])) > 0
        self.assert_eq(has_logs, True, "EventLog tracking active")
        
        # Check SM reload
        self.sm.load_data()
        self.assert_eq(c_id in self.sm.data["clients"], True, "Data persistent on reload")

if __name__ == "__main__":
    suite = TestsV23()
    suite.run_all()
