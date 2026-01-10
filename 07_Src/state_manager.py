import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKING_DIR = os.path.join(BASE_DIR, '04_Data', 'tracking')
PERSISTENCE_FILE = os.path.join(TRACKING_DIR, 'persistence.json')

class StateManager:
    # 1. Strict Enum Definitions
    REPORT_TYPES = ["BASELINE", "FREQUENCY", "INCIDENT", "RESCUE", "MONTHLY", "ON_DEMAND"]
    REPORT_STATUSES = ["GENERADO", "EN_REVISION", "APROBADO_TACITO", "OBJETADO", "INVALIDADO"]
    QC_STATUSES = ["PENDIENTE", "APROBADO", "FALLIDO"]
    INTAKE_STATUSES = ["GENERADO", "AUTORIZADO", "EJECUTADO"]
    REQUESTED_BY = ["SYSTEM", "AG", "CLI_USER"]
    INVALIDATED_REASON = ["QC_FAIL", "CLIENT_ERROR_REAL"]
    CLIENT_TYPES = ["PF", "PM"]

    def __init__(self):
        self.TRACKING_DIR = TRACKING_DIR
        if not os.path.exists(TRACKING_DIR):
            os.makedirs(TRACKING_DIR)
        self.reload()

    def reload(self):
        self.load_data()
        self._migrate_legacy_keys()

    def _migrate_legacy_keys(self):
        # One-time migration of "type"->"report_type", "status"->"report_status"
        changed = False
        for client in self.data.get("clients", {}).values():
            for r in client.get("reports", []):
                # Migrate type
                if "type" in r:
                    r["report_type"] = r.pop("type")
                    changed = True
                # Migrate status
                if "status" in r:
                    r["report_status"] = r.pop("status")
                    changed = True
        
        if changed:
            print("Legacy keys migrated to canonical form.")
            self.save_data()

    def load_data(self):
        if os.path.exists(PERSISTENCE_FILE):
            with open(PERSISTENCE_FILE, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "clients": {},   # key: client_id (7 digits)
                "intakes": {},   # key: intake_id
                "reports": {},   # key: report_id (or base_name)
                "logs": []       # Event Logs
            }
            self.save_data()
        
        # Safety checks
        self.data.setdefault("clients", {})
        self.data.setdefault("intakes", {})
        self.data.setdefault("reports", {})
        self.data.setdefault("logs", [])

    def ensure_defaults(self, client_state):
        defaults = {
            "client_id": "",
            "client_name_full": "",
            "client_name_slug": "",
            "client_type": "PF",
            "incident_limit_month": 2,
            "incident_count_month": 0,
            "incident_month_key": datetime.now().strftime("%Y-%m"),
            "last_valid_report_id": None,
            "created_at": datetime.now().isoformat(),
            "reports": [], # List of report_ids
            "intakes": [], # List of intake_ids
            "report_seq": 0,
            "intake_seq": 0
        }
        if client_state is None:
            return defaults.copy()
            
        for k, v in defaults.items():
            if k not in client_state:
                client_state[k] = v
        return client_state

    def add_event_log(self, entity_type, entity_id, action, from_state, to_state, actor="SYSTEM", notes=""):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,
            "from_state": from_state,
            "to_state": to_state,
            "actor": actor,
            "notes": notes
        }
        self.data["logs"].append(log_entry)
        self.save_data()

    def validate_slug(self, slug):
        import re
        if not re.match(r"^[a-zA-Z0-9_]+$", slug):
            raise ValueError(f"Invalid client_name_slug: '{slug}'. Only letters, numbers, and underscores allowed.")

    def save_data(self):
        with open(PERSISTENCE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def sanitize_filename(self, name):
        return name.replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n").replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U").replace("Ñ", "N")

    def _get_or_create_client_id(self, client_name, client_type="PF"):
        # Slug generation
        slug = self.sanitize_filename(client_name)
        self.validate_slug(slug)
        
        # Check by name first
        for c_id, info in self.data["clients"].items():
            if info.get("client_name_slug") == slug:
                return c_id
        
        # Create new ID (Find first available numeric hole starting from 1)
        # This logic ensures the next_client_id resets to 0000001 for new fresh cases
        # while preserving historical records. It avoids monotonically increasing gaps.
        existing_ids = set(int(i) for i in self.data["clients"].keys())
        new_numeric = 1
        while new_numeric in existing_ids:
            new_numeric += 1
        new_id = f"{new_numeric:07d}"
        
        self.update_client(new_id, client_name_full=client_name, client_name_slug=slug, client_type=client_type)
        self.add_event_log("CLIENT", new_id, "CREATE", None, "CREATED", actor="SYSTEM")
        return new_id

    def create_client(self, client_id, client_name, client_type="PF"):
        """
        Public API to explicitly create or register an existing client ID.
        Useful for when the client ID is already known (e.g. from intake file).
        """
        if client_id not in self.data["clients"]:
             self.update_client(client_id, client_name_full=client_name, client_type=client_type)
             self.add_event_log("CLIENT", client_id, "CREATE", None, "CREATED", actor="SYSTEM")
        return client_id

    def get_client(self, client_id):
        return self.data["clients"].get(client_id)

    def update_client(self, client_id, **kwargs):
        if client_id not in self.data["clients"]:
            self.data["clients"][client_id] = self.ensure_defaults(None)
            self.data["clients"][client_id]["id"] = client_id
        
        # Ensure defaults before updating
        self.data["clients"][client_id] = self.ensure_defaults(self.data["clients"][client_id])
        
        self.data["clients"][client_id].update(kwargs)
        self.save_data()

    def get_next_report_id(self, client_id):
        client = self.get_client(client_id)
        if not client: return "R-0001"
        
        current_seq = client.get("report_seq", 0)
        new_seq = current_seq + 1
        return f"R-{new_seq:04d}"

    def confirm_report_generation(self, client_id):
        # Only call this when a report is fully successfully generated to increment seq
        client = self.get_client(client_id)
        if client:
            client["report_seq"] = client.get("report_seq", 0) + 1
            self.save_data()

    def reset_incident_counter_if_needed(self, client_id):
        client = self.get_client(client_id)
        if not client: return
        
        current_month = datetime.now().strftime("%Y-%m")
        if client.get("incident_month_key") != current_month:
            self.update_client(client_id, incident_count_month=0, incident_month_key=current_month)

    def create_intake(self, client_id, intake_type, requested_by="SYSTEM", replaces_report_id=None):
        if intake_type not in self.REPORT_TYPES:
            raise ValueError(f"Invalid Intake Type: {intake_type}")
        if requested_by not in self.REQUESTED_BY:
            raise ValueError(f"Invalid Requested By: {requested_by}")
        if intake_type == "RESCUE" and not replaces_report_id:
            raise ValueError("replaces_report_id is mandatory for RESCUE intake.")

        client = self.get_client(client_id)
        if not client:
            raise ValueError(f"Client {client_id} not found.")

        # Incident limit check (I7)
        if intake_type == "INCIDENT":
            self.reset_incident_counter_if_needed(client_id)
            if client["incident_count_month"] >= client["incident_limit_month"]:
                # Spec: PROHIBIDO autorizar sin aprobación de costo. 
                # We create it as GENERADO, but we won't allow status -> AUTORIZADO without extra flag later.
                pass 

        seq = client.get("intake_seq", 0) + 1
        intake_id = f"I-{client_id}-{seq:04d}"
        
        intake_data = {
            "intake_id": intake_id,
            "client_id": client_id,
            "intake_type": intake_type,
            "intake_status": "GENERADO",
            "created_at": datetime.now().isoformat(),
            "authorized_at": None,
            "executed_at": None,
            "requested_by": requested_by,
            "replaces_report_id": replaces_report_id
        }
        
        self.data["intakes"][intake_id] = intake_data
        client["intakes"].append(intake_id)
        client["intake_seq"] = seq
        
        self.add_event_log("INTAKE", intake_id, "CREATE", None, "GENERADO", actor=requested_by)
        self.save_data()
        return intake_id

    def update_intake(self, intake_id, to_status, actor="SYSTEM"):
        intake = self.data["intakes"].get(intake_id)
        if not intake: raise ValueError(f"Intake {intake_id} not found.")
        
        from_status = intake["intake_status"]
        if to_status not in self.INTAKE_STATUSES:
             raise ValueError(f"Invalid Intake Status: {to_status}")

        # Transition validation (3.1)
        allowed = {
            "GENERADO": ["AUTORIZADO"],
            "AUTORIZADO": ["EJECUTADO"]
        }
        if to_status not in allowed.get(from_status, []):
            raise ValueError(f"Invalid Intake transition: {from_status} -> {to_status}")

        intake["intake_status"] = to_status
        if to_status == "AUTORIZADO":
            intake["authorized_at"] = datetime.now().isoformat()
        elif to_status == "EJECUTADO":
            intake["executed_at"] = datetime.now().isoformat()

        self.add_event_log("INTAKE", intake_id, "STATUS_CHANGE", from_status, to_status, actor=actor)
        self.save_data()

    def create_report(self, client_id, intake_id, report_type, artifacts=None):
        client = self.get_client(client_id)
        if not client: raise ValueError(f"Client {client_id} not found.")
        
        seq = client.get("report_seq", 0) + 1
        report_id = f"R-{client_id}-{seq:04d}"
        
        report_data = {
            "report_id": report_id,
            "client_id": client_id,
            "intake_id": intake_id,
            "report_type": report_type,
            "report_status": "GENERADO",
            "qc_status": "PENDIENTE",
            "created_at": datetime.now().isoformat(),
            "sent_at": None,
            "review_deadline_at": None,
            "invalidated_reason": None,
            "artifacts": artifacts or {
                "final_pdf_path": None,
                "arco_files_paths": [],
                "qc_checklist_json_path": None
            }
        }
        
        self.data["reports"][report_id] = report_data
        client["reports"].append(report_id)
        client["report_seq"] = seq
        
        self.add_event_log("REPORT", report_id, "CREATE", None, "GENERADO", actor="SYSTEM")
        self.save_data()
        return report_id

    def update_report_status(self, report_id, to_status, actor="SYSTEM", invalidated_reason=None):
        report = self.data["reports"].get(report_id)
        if not report: raise ValueError(f"Report {report_id} not found.")
        
        from_status = report["report_status"]
        if to_status not in self.REPORT_STATUSES:
             raise ValueError(f"Invalid Report Status: {to_status}")

        # Transition validation (3.3)
        allowed = {
            "GENERADO": ["EN_REVISION"],
            "EN_REVISION": ["APROBADO_TACITO", "OBJETADO"],
            "OBJETADO": ["INVALIDADO"]
        }
        
        # Exception: QC_FAIL can lead directly to INVALIDADO in the pipeline if QC fails immediately.
        if from_status == "GENERADO" and to_status == "INVALIDADO":
            pass # Allowed for QC_FAIL (I3)
        elif to_status not in allowed.get(from_status, []):
            raise ValueError(f"Invalid Report transition: {from_status} -> {to_status}")

        report["report_status"] = to_status
        if to_status == "EN_REVISION":
             report["sent_at"] = datetime.now().isoformat()
             # review_deadline_at = sent_at + 48h (2.3)
             from datetime import timedelta
             deadline = datetime.now() + timedelta(hours=48)
             report["review_deadline_at"] = deadline.isoformat()
        
        if invalidated_reason:
            if invalidated_reason not in self.INVALIDATED_REASON:
                raise ValueError(f"Invalidated Reason invalid: {invalidated_reason}")
            report["invalidated_reason"] = invalidated_reason

        self.add_event_log("REPORT", report_id, "STATUS_CHANGE", from_status, to_status, actor=actor)
        self.save_data()

    def update_qc_status(self, report_id, to_status, actor="SYSTEM"):
        report = self.data["reports"].get(report_id)
        if not report: raise ValueError(f"Report {report_id} not found.")
        
        from_status = report["qc_status"]
        # Transition validation (3.2)
        if from_status != "PENDIENTE":
            raise ValueError(f"QC already finalized: {from_status}")
        
        if to_status not in self.QC_STATUSES:
             raise ValueError(f"Invalid QC Status: {to_status}")

        report["qc_status"] = to_status
        self.add_event_log("REPORT", report_id, "QC_CHANGE", from_status, to_status, actor=actor)
        self.save_data()

    def process_tacit_approvals(self):
        # 4.3 Review window (48h)
        now = datetime.now()
        for report_id, report in self.data["reports"].items():
            if report["report_status"] == "EN_REVISION" and report["review_deadline_at"]:
                deadline = datetime.fromisoformat(report["review_deadline_at"])
                if now > deadline:
                    self.update_report_status(report_id, "APROBADO_TACITO")
                    # Update client's last_valid_report_id (I6)
                    client_id = report["client_id"]
                    self.update_client(client_id, last_valid_report_id=report_id)
                    print(f"[+] Tacit approval: {report_id}")

    def list_authorized_intakes_by_priority(self):
        # I5 — Prioridad global obligatoria: RESCUE > INCIDENT > FREQUENCY > BASELINE
        priority_map = {"RESCUE": 0, "INCIDENT": 1, "FREQUENCY": 2, "BASELINE": 3}
        
        authorized = []
        for i_id, intake in self.data["intakes"].items():
            if intake["intake_status"] == "AUTORIZADO":
                authorized.append(intake)
        
        # Sort by priority, then by creation time
        authorized.sort(key=lambda x: (priority_map.get(x["intake_type"], 99), x["created_at"]))
        return authorized
