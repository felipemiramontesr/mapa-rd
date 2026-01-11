import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from notifier import Notifier
from config_manager import ConfigManager

def test_live_email():
    """Send a real email to verify HTML template."""
    print("[*] Starting Live Email Test...")
    
    # 1. Load Secrets directly (Simulating Production Environment)
    try:
        secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '03_Config', 'secrets.json')
        with open(secrets_path, 'r', encoding='utf-8-sig') as f:
            secrets = json.load(f)
            smtp_conf = secrets.get("smtp", {})
    except Exception as e:
        print(f"[!] Failed to load secrets: {e}")
        return

    # 2. Configure Notifier with SMTP backend and Credentials
    config_override = {
        "backend": "smtp",
        "sender_email": smtp_conf.get("smtp_user"), 
        "smtp_host": smtp_conf.get("smtp_host"),
        "smtp_port": smtp_conf.get("smtp_port"),
        "smtp_user": smtp_conf.get("smtp_user"),
        "smtp_pass": smtp_conf.get("smtp_pass"),
        "smtp_tls": True
    }

    if not config_override["smtp_pass"]:
        print("[!] No SMTP Password found in secrets.json. Cannot Proceed.")
        return

    notifier = Notifier(config_override)
    
    # 3. Send Test
    target_email = "felipemiramontesr@gmail.com"
    print(f"[*] Sending to: {target_email}")
    
    success, msg = notifier.send_report(
        receiver_emails=[target_email],
        report_path=None, # Only testing body template
        client_name="Felipe Miramontes (Admin)",
        scan_id="TEST-LIVE-001",
        subject="MAPA-RD: Premium HTML Template Verification"
    )
    
    if success:
        print(f"[SUCCESS] Email dispatched. ID: {msg}")
        print("Please check inbox for HTML formatting.")
    else:
        print(f"[FAILURE] {msg}")

if __name__ == "__main__":
    test_live_email()
