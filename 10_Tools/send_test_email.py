import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from notifier import Notifier

def send_test(recipients):
    print(f"[*] Sending Test Email to: {recipients}")
    
    # Check config
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '03_Config', 'config.json')
    with open(config_path, 'r') as f:
        cfg = json.load(f)
        
    print(f"[*] Using SMTP Server: {cfg['email'].get('smtp_host')}")
    print(f"[*] Sender: {cfg['email']['sender_email']}")
    
    notifier = Notifier()
    
    # We use arguments compatible with send_report:
    # client_email, report_path, report_id
    
    # Since Notifier.send_report is designed for a single recipient string, 
    # we will iterate if multiple are passed, OR modify notifier.
    # But usually notifier takes "client_email" as a string.
    
    # Let's create a dummy dummy PDF if needed, or just send text?
    # Notifier code:
    # def send_report(self, client_email, report_path, report_id):
    
    # Let's create a dummy file to attach
    dummy_pdf = "TEST_ATTACHMENT.txt"
    with open(dummy_pdf, "w") as f:
        f.write("This is a test attachment from MAPA-RD.")
        
    for recipient in recipients:
        print(f"    -> Sending to {recipient}...")
        try:
            notifier.send_report(recipient, dummy_pdf, "TEST-001-MANUAL")
            print(f"    [+] Success for {recipient}")
        except Exception as e:
            print(f"    [!] Failed for {recipient}: {e}")
            
    # Cleanup
    if os.path.exists(dummy_pdf):
        os.remove(dummy_pdf)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_test_email.py email1 email2 ...")
        sys.exit(1)
        
    recipients = sys.argv[1:]
    send_test(recipients)
