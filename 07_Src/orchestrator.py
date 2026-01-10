import os
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional

# Internal Core Modules
from state_manager import StateManager
from qc_manager import QCManager
from normalizer import Normalizer
from scorer import Scorer
from report_generator import ReportGenerator
from notifier import Notifier

class Orchestrator:
    """The central brain of MAPA-RD.
    
    Coordinates data collection (SpiderFoot), processing (Normalized/Scorer),
    artifact generation, quality control gates, and notification dispatch.
    """

    def __init__(self):
        """Initialize core components and load environmental configurations."""
        self.sm = StateManager()
        self.qc = QCManager(self.sm)
        self.rg = ReportGenerator(self.sm)
        self.notifier = Notifier()
        
        # Default infrastructure settings
        self.spiderfoot_path = "."
        self.python_exe = "python"
        self._load_config()
        
        self.sf_script = os.path.join(self.spiderfoot_path, "sf.py")

    def _load_config(self) -> None:
        """Load external tool path configurations."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '03_Config', 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    self.spiderfoot_path = cfg.get("spiderfoot_path", ".")
                    self.python_exe = cfg.get("python_exe", "python")
            except (json.JSONDecodeError, IOError) as e:
                print(f"[!] Warning: Config loading failed: {e}")

    def run_spiderfoot_scan(self, target: str, scan_id: str) -> List[Dict[str, Any]]:
        """Execute a SpiderFoot CLI scan or fallback to simulation.
        
        Args:
            target: Domain or email to scan.
            scan_id: Identifier for logging.
            
        Returns:
            A list of SpiderFoot event dictionaries.
        """
        if not os.path.exists(self.sf_script):
            print(f"[!] MOCK MODE: SpiderFoot not found at {self.sf_script}. Returning stub data.")
            return [{"source": "sfp_citadel", "entity": "MOCK_FINDING", "risk_score": "P0"}]

        cmd = [self.python_exe, self.sf_script, "-s", target, "-o", "json", "-q"]
        print(f"[*] Executing SpiderFoot: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=600) # nosec
            if result.returncode != 0:
                print(f"[!] CLI Error: {result.stderr}")
                return []
            
            events = []
            for line in result.stdout.splitlines():
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return events
        except (subprocess.SubprocessError, Exception) as e:
            print(f"[!] Scan Exception: {e}")
            return []

    def orchestrate(self, client_id: str, analysis_type: str = "monthly") -> Tuple[str, str]:
        """Ad-hoc entry point for CLI-driven scans.
        
        Args:
            client_id: Target client identifier.
            analysis_type: Report frequency/type.
            
        Returns:
            A tuple of (intake_id, client_directory).
        """
        intake_type = analysis_type.upper() if analysis_type else "ON_DEMAND"
        
        # Ensure client exists in state
        if not self.sm.get_client(client_id):
             self.sm.create_client(client_id, client_id)

        intake_id = self.sm.create_intake(client_id, intake_type, requested_by="CLI_USER")
        self.sm.update_intake(intake_id, "AUTORIZADO", actor="CLI_USER")
        
        self.execute_pipeline(intake_id)
        
        client = self.sm.get_client(client_id)
        client_dir = client.get("client_dir", client_id) if client else client_id
        return intake_id, client_dir

    def execute_pipeline(self, intake_id: str) -> None:
        """Run the full intake-to-report lifecycle.
        
        Args:
            intake_id: The ID of the authorized intake to process.
        """
        intake = self.sm.data["intakes"].get(intake_id)
        if not intake:
            return
        
        client_id = intake["client_id"]
        client = self.sm.get_client(client_id)
        if not client:
             return
        
        print(f"\n[PIPELINE START] {intake_id} | Client: {client['client_name_full']}")

        # 1. Start execution
        self.sm.update_intake(intake_id, "EJECUTADO")
        
        # 2. Intel Gathering
        target = self._resolve_target(intake, client)
        raw_data = self.run_spiderfoot_scan(target, intake_id)
        
        # Persistence
        raw_path = self._persist_raw_data(client["client_dir"], intake_id, raw_data)
        
        # 3. Processing
        print("[*] Processing intelligence...")
        norm = Normalizer().normalize_scan(raw_data)
        scored = Scorer().score_findings(norm)
        
        # 4. Artifact Generation
        report_id = self.sm.create_report(client_id, intake_id, intake["intake_type"])
        art = self.rg.generate_report(client_id, intake_id, report_id, scored, intake["intake_type"])
        
        self.sm.data["reports"][report_id]["artifacts"].update({
            "final_pdf_path": art["pdf_path"],
            "arco_files_paths": [art["arco_dir"]] if art.get("arco_dir") else []
        })
        self.sm.save_data()

        # 5. Quality Control Gate
        if self._run_qc_gate(report_id, art):
            self._dispatch_notification(report_id, client, intake, art["pdf_path"])
        else:
            self._handle_qc_failure(client_id, report_id)

    def _resolve_target(self, intake: Dict[str, Any], client: Dict[str, Any]) -> str:
        """Pick the best target (Domain > Email > Slug) for scanning."""
        ident = intake.get("identity", {})
        if ident.get("domains"): return ident["domains"][0]
        if ident.get("emails"): return ident["emails"][0]
        return client["client_name_slug"]

    def _persist_raw_data(self, client_dir: str, intake_id: str, data: List[Dict[str, Any]]) -> str:
        """Save raw findings to the data directory."""
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '04_Data', 'raw', client_dir, intake_id)
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, 'spiderfoot.json')
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return full_path

    def _run_qc_gate(self, report_id: str, artifacts: Dict[str, Any]) -> bool:
        """Run the quality checklist and log results."""
        res = self.qc.run_qc_checklist(report_id, artifacts["pdf_path"])
        qc_file = artifacts["pdf_path"].replace("REPORTE", "QC").replace(".pdf", ".json")
        with open(qc_file, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=4)
        
        self.sm.update_qc_status(report_id, res["qc_status"])
        self.sm.data["reports"][report_id]["artifacts"]["qc_checklist_json_path"] = qc_file
        self.sm.save_data()
        return res["qc_status"] == "APROBADO"

    def _dispatch_notification(self, report_id: str, client: Dict[str, Any], intake: Dict[str, Any], pdf_path: str) -> None:
        """Send the report to the client and admin."""
        recipients = list(intake.get("identity", {}).get("emails", []))
        if not recipients: recipients = ["unknown@example.com"]
        
        admin_copy = "info@felipemiramontesr.net"
        if admin_copy not in recipients: recipients.append(admin_copy)

        success, msg_id = self.notifier.send_report(recipients, pdf_path, client["client_name_full"], scan_id=report_id)
        if success:
            self.sm.update_report_status(report_id, "EN_REVISION")
            print(f"[+] Pipeline COMPLETED for {report_id}")
        else:
            print(f"[!] Notification failed for {report_id}")

    def _handle_qc_failure(self, client_id: str, report_id: str) -> None:
        """Process a failed QC gate by invalidating the report and creating a rescue intake."""
        print(f"[!] QC Failure for {report_id}. Invalidating and creating RESCUE.")
        self.sm.update_report_status(report_id, "INVALIDADO", actor="SYSTEM", invalidated_reason="QC_FAIL")
        rescue_id = self.sm.create_intake(client_id, "RESCUE", requested_by="SYSTEM", replaces_report_id=report_id)
        print(f"[+] RESCUE created: {rescue_id}")

    def run_automatic_scheduler(self) -> None:
        """Scan all authorized intakes according to priority rules."""
        pending = self.sm.list_authorized_intakes_by_priority()
        print(f"[*] Scheduler: {len(pending)} pending tasks.")
        for task in pending:
            try:
                self.execute_pipeline(task["intake_id"])
            except Exception as e:
                print(f"[CRITICAL] Intake {task['intake_id']} failed: {e}")

if __name__ == "__main__":
    Orchestrator().run_automatic_scheduler()
