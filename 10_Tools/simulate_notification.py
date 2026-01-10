import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from notifier import Notifier

def simulate_real_notification():
    recipients = ["info@felipemiramontesr.net", "felipemiramontesr@gmail.com"]
    dummy_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pwned_message.pdf")
    
    # Verify PDF exists
    if not os.path.exists(dummy_pdf):
        print(f"[!] Critical: {dummy_pdf} not found. Did pandoc run?")
        return

    print("[*] Initializing Notifier (Production Mode)...")
    notifier = Notifier()
    
    print(f"[*] Sending Simulation to: {recipients}")
    
    # We send one email per recipient in loop to simulate individual reports, or one email to multiple?
    # The Orchestrator sends to a LIST of emails for a SINGLE client.
    # So we pass the list directly.
    
    # Mock Data
    client_name = "Felipe Miramontes (Simulación)"
    scan_id = "R-SIM-2026-001"
    
    try:
        success, msg_id = notifier.send_report(
            recipients, 
            dummy_pdf, 
            client_name, 
            scan_id=scan_id
        )
        
        if success:
            print(f"[+] Email Sent Successfully! Message ID: {msg_id}")
            print("    -> Check inbox for Subject like: 'Reporte MAPA-RD #001 | Felipe Miramontes...'")
        else:
            print(f"[!] Email Failed: {msg_id}")
            
    except Exception as e:
        print(f"[!] Critical Error: {e}")
    finally:
        if os.path.exists(dummy_pdf):
            os.remove(dummy_pdf)

if __name__ == "__main__":
    simulate_real_notification()
