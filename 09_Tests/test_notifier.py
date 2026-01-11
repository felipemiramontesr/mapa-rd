import pytest
import os
import glob
import sys
# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))
from notifier import Notifier

class TestNotifier:
    def test_stub_email_generation(self):
        """Verify that the Stub backend correctly 'sends' emails by writing JSON files."""
        # 1. Setup with explicit 'backend' key
        config = {
            "backend": "stub",
            "sender_email": "test@mapa-rd.com"
        }
        notifier = Notifier(config_dict=config)
        
        # Clean outbox before test
        files = glob.glob(os.path.join(notifier.outbox_dir, "*.json"))
        for f in files:
            try: os.remove(f)
            except: pass
            
        subject = "TEST EMAIL"
        body = "This is a test body."
        
        # 2. Execute
        result, msg_id = notifier.send_report(
            receiver_emails=["client@example.com"],
            report_path=None,
            client_name="Test Client",
            subject=subject,
            body=body,
            scan_id="R-TEST-001"
        )
        
        # 3. Assertions
        assert result is True
        assert msg_id is not None
        
        # Verify file creation
        outbox_files = glob.glob(os.path.join(notifier.outbox_dir, "*_R-TEST-001.json"))
        assert len(outbox_files) == 1
        assert os.path.exists(outbox_files[0])
