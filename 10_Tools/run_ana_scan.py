import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from orchestrator import Orchestrator

def main():
    print("[*] Starting Pipeline for Ana Flores...")
    orc = Orchestrator()
    
    client_id = "ana-flores"
    client_name = "Ana Flores"
    email = "anafbaca@gmail.com"
    
    # 1. Ensure Client Exists
    if client_id not in orc.sm.data.get("clients", {}):
        print(f"[*] Registering new client: {client_id}")
        orc.sm.create_client(client_id, client_name)
    
    # 2. Create Intake via API (Ensures State Tracking)
    # We pass the identity details here.
    # Note: create_intake signature might not accept identity dict directly?
    # Let's check state_manager.py or assume we update it after creation.
    # Usually create_intake just sets basic metadata.
    
    print("[*] Creating Intake...")
    intake_id = orc.sm.create_intake(client_id, "ON_DEMAND", requested_by="CLI_USER")
    print(f"[+] Intake Created: {intake_id}")
    
    # 3. Update Intake with Identity Details (Crucial for target selection)
    # We access the dict directly in memory or via update method?
    # sm.update_intake updates status mostly.
    # Let's modify the data object directly and save.
    orc.sm.data["intakes"][intake_id]["identity"] = {
        "names": [client_name],
        "emails": [email],
        "domains": [],
        "usernames": []
    }
    orc.sm.save_data()
    
    # 4. Autorizar (Intake flow requires authorization usually)
    orc.sm.update_intake(intake_id, "AUTORIZADO", actor="AdminScript")
    
    # 5. Execute
    print(f"[*] Executing Pipeline for {intake_id}...")
    orc.execute_pipeline(intake_id)
    print("[+] Pipeline Finished.")

if __name__ == "__main__":
    main()
