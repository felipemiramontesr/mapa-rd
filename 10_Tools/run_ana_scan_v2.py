import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from orchestrator import Orchestrator

def main():
    print("[*] Starting Pipeline for Ana Flores (Attempt 2 - Full Free Profile)...")
    orc = Orchestrator()
    
    client_id = "ana-flores"
    client_name = "Ana Flores"
    email = "anafbaca@gmail.com"
    
    # 1. Ensure Client Exists
    if client_id not in orc.sm.data.get("clients", {}):
        print(f"[*] Registering new client: {client_id}")
        orc.sm.create_client(client_id, client_name)
    
    # 2. Create Intake
    print("[*] Creating Intake...")
    intake_id = orc.sm.create_intake(client_id, "ON_DEMAND", requested_by="CLI_USER")
    print(f"[+] Intake Created: {intake_id}")
    
    # 3. Update Identity
    orc.sm.data["intakes"][intake_id]["identity"] = {
        "names": [client_name],
        "emails": [email],
        "domains": [],
        "usernames": []
    }
    orc.sm.save_data()
    
    # 4. Autorizar
    orc.sm.update_intake(intake_id, "AUTORIZADO", actor="AdminScript")
    
    # 5. Execute
    print(f"[*] Executing Pipeline for {intake_id}...")
    orc.execute_pipeline(intake_id)
    print("[+] Pipeline Finished.")

if __name__ == "__main__":
    main()
