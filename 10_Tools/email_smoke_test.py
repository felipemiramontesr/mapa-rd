
import os
import sys
import json
import uuid
import time
from datetime import datetime

# Add src to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from notifier import Notifier

def run_smoke_test():
    print("="*60)
    print(f"MAPA-RD EMAIL SMOKE TEST | {datetime.now().isoformat()}")
    print("="*60)

    # Init Notifier (reads env/config)
    try:
        notifier = Notifier(config_path=os.path.join(BASE_DIR, "config", "config.json"))
        print(f"[*] Configuration Loaded")
        print(f"[*] Backend: {notifier.backend}")
        if notifier.backend == "smtp":
            print(f"[*] Host: {notifier.config.get('smtp_host')}")
            print(f"[*] User: {notifier.config.get('smtp_user')}")
    except Exception as e:
        print(f"[!] Init Failed: {e}")
        return

    # Prepare Target
    target = os.getenv("EMAIL_SMOKE_TEST_TO") or notifier.config.get("sender_email")
    if not target:
        print("[!] No target email found. Set EMAIL_SMOKE_TEST_TO env var.")
        return
        
    print(f"[*] Target: {target}")

    # Generate Test Message
    test_id = str(uuid.uuid4())
    msg = f"MAPA-RD SMTP SMOKE TEST\nTimestamp: {datetime.now()}\nTest ID: {test_id}\n\nIf you received this, the backend is accepted."
    
    # We need to hack the send_report slightly or just use private methods?
    # ActuallyNotifier.send_report requires a file path. Let's create a dummy file.
    dummy_file = os.path.join(BASE_DIR, "data", "test", f"smoke_{test_id}.txt")
    os.makedirs(os.path.dirname(dummy_file), exist_ok=True)
    with open(dummy_file, "w") as f:
        f.write(msg)

    print("[*] Sending test email...")
    start = time.time()
    
    success, result = notifier.send_report([target], dummy_file, "SMOKE_TEST_CLIENT", scan_id=f"SMOKE-{test_id}")
    
    duration = int((time.time() - start) * 1000)
    
    # Clean up
    if os.path.exists(dummy_file):
        os.remove(dummy_file)

    # Log Result
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "backend": notifier.backend,
        "success": success,
        "result": result, # message_id or error
        "duration_ms": duration
    }
    
    log_file = "email_smoke_log.json"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
        
    print("-" * 60)
    if success:
        print(f"[SUCCESS] Message accepted.")
        print(f"Message ID: {result}")
    else:
        print(f"[FAIL] Error: {result}")
    print(f"Duration: {duration}ms")
    print("="*60)

if __name__ == "__main__":
    run_smoke_test()
