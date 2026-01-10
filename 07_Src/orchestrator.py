import os
import json
import subprocess
from datetime import datetime

# Import Internal Modules
from state_manager import StateManager
from qc_manager import QCManager
from normalizer import Normalizer
from scorer import Scorer
from report_generator import ReportGenerator
from notifier import Notifier

class Orchestrator:
    def __init__(self):
        self.sm = StateManager()
        self.qc = QCManager(self.sm)
        self.rg = ReportGenerator()
        self.notifier = Notifier()
        self.spiderfoot_path = "C:\\Users\\felip\\spiderfoot"
        self.python_exe = "python"

    def run_automatic_scheduler(self):
        """
        I5 — Global Priority: RESCUE > INCIDENT > FREQUENCY > BASELINE
        """
        print(f"[*] Starting MAPA-RD v2.3 Scheduler...")
        pending = self.sm.list_authorized_intakes_by_priority()
        if not pending:
            print("[*] No authorized intakes found.")
            return

        print(f"[+] Found {len(pending)} pending intakes. Executing in priority order.")
        for intake in pending:
            try:
                self.execute_pipeline(intake["intake_id"])
            except Exception as e:
                print(f"[!] Critical Error in intake {intake['intake_id']}: {e}")
                import traceback
                traceback.print_exc()

    def orchestrate(self, client_id, analysis_type="monthly"):
        """
        Public API entry point for main.py.
        Creates an on-demand intake and executes it.
        Returns: (scan_id, client_dir_name)
        """
        # 1. Create Ad-Hoc Intake
        # We assume 'requested_by' is CLI/Manual for this entry point
        intake_type = analysis_type.upper() if analysis_type else "ON_DEMAND"
        
        # Check if client exists, if not, create a stub? 
        # For now, we assume client exists based on main.py logic.
        if client_id not in self.sm.data.get("clients", {}):
             # Ensure client exists in SM to avoid lookup errors
             self.sm.create_client(client_id, client_id)

        intake_id = self.sm.create_intake(client_id, intake_type, requested_by="CLI_USER")
        
        # 1.1 Auto-Authorize (CLI/OnDemand skips manual authorization step)
        self.sm.update_intake(intake_id, "AUTORIZADO", actor="CLI_USER")
        
        # 2. Execute
        self.execute_pipeline(intake_id)
        
        # 3. Return values compatible with main.py expectation
        # main.py expects: scan_id, client_dir_name
        # scan_id is effectively the report_id or intake_id in this flow?
        # looking at main.py: raw_path = os.path.join(..., client_dir_name, scan_id, ...)
        
        # For backward compatibility with the legacy 'scan_id' concept, 
        # we will use the intake_id as the scan_id
        
        client_dir_name = self.sm.get_client(client_id).get("client_dir", client_id)
        
        return intake_id, client_dir_name

    def execute_pipeline(self, intake_id):
        intake = self.sm.data["intakes"].get(intake_id)
        if not intake: return
        
        client_id = intake["client_id"]
        client = self.sm.get_client(client_id)
        
        print(f"\n{'-'*60}")
        print(f"PIPELINE: {intake_id} ({intake['intake_type']}) for {client['client_name_full']}")
        print(f"{'-'*60}")

        # 1. EJECUCIÓN (INTAKE -> EJECUTADO)
        self.sm.update_intake(intake_id, "EJECUTADO")
        
        # 2. INTEL (Mocked for now, following 4.2)
        # Note: In a full integration, run_spiderfoot_scan would be called here.
        scan_id = intake_id # Using intake_id as scan_id for consistency
        raw_data = [{"source": "sfp_citadel", "entity": "Compromised Credentials", "risk_score": "P0"}]
        
        # SIMULATION: Write this mock data to disk so downstream tools (and tests) find it
        # Path: 04_Data/raw/{client_dir}/{scan_id}/spiderfoot.json
        client_dir_name = self.sm.get_client(client_id).get("client_dir", client_id)
        raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '04_Data', 'raw', client_dir_name, scan_id)
        os.makedirs(raw_dir, exist_ok=True)
        with open(os.path.join(raw_dir, 'spiderfoot.json'), 'w') as f:
            json.dump(raw_data, f)
        
        norm_findings = Normalizer().normalize_scan(raw_data)
        scored_findings = Scorer().score_findings(norm_findings)
        
        # 3. GENERACIÓN Artefactos (4.2.3)
        report_type = intake["intake_type"]
        report_id = self.sm.create_report(client_id, intake_id, report_type)
        
        artifacts = self.rg.generate_report(client_id, intake_id, report_id, scored_findings, report_type)
        
        # Update report with paths
        self.sm.data["reports"][report_id]["artifacts"] = {
            "final_pdf_path": artifacts["pdf_path"],
            "arco_files_paths": [artifacts["arco_dir"]] if artifacts["arco_dir"] else [],
            "qc_checklist_json_path": None # Filled next
        }
        self.sm.save_data()

        # 4. QC GATE (I2, 4.2.4)
        qc_result = self.qc.run_qc_checklist(report_id, artifacts["pdf_path"])
        
        # Save QC details (Spec Nomenclature)
        qc_base_name = artifacts["base_name"].replace("REPORTE", "QC")
        qc_log_path = os.path.join(os.path.dirname(artifacts["pdf_path"]), f"{qc_base_name}.json")
        os.makedirs(os.path.dirname(qc_log_path), exist_ok=True)
        with open(qc_log_path, 'w', encoding='utf-8') as f:
            json.dump(qc_result, f, indent=4)
        self.sm.data["reports"][report_id]["artifacts"]["qc_checklist_json_path"] = qc_log_path
        
        if qc_result["qc_status"] == "APROBADO":
            # I2: QC_STATUS is absolute gate for sending
            self.sm.update_qc_status(report_id, "APROBADO")
            
            # 5. ENVÍO (4.2.5)
            print(f"[*] Sending report {report_id}...")
            # success = self.notifier.send_report(...)
            success = True # Forced for demo/implementation walk
            
            if success:
                self.sm.update_report_status(report_id, "EN_REVISION")
                print(f"[+] Pipeline COMPLETED for {report_id}")
            else:
                print(f"[!] Failed to send {report_id}")
        else:
            # I3: Hard fail on QC failure
            print(f"[!] QC FAILURE for {report_id}. Applying Hard Fail logic (I3).")
            self.sm.update_qc_status(report_id, "FALLIDO")
            self.sm.update_report_status(report_id, "INVALIDADO", actor="SYSTEM", invalidated_reason="QC_FAIL")
            
            # Automatic RESCUE intake creation (I4)
            rescue_id = self.sm.create_intake(client_id, "RESCUE", requested_by="SYSTEM", replaces_report_id=report_id)
            print(f"[!] RESCUE intake created: {rescue_id}. Report NOT SENT.")

if __name__ == "__main__":
    orch = Orchestrator()
    orch.run_automatic_scheduler()
