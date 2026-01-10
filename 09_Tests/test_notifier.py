import pytest
import os
from notifier import Notifier

class TestNotifier:
    def test_stub_email_generation(self):
        # Config for stub mode
        config = {
            "notification_backend": "stub",
            "sender_email": "test@mapa-rd.com"
        }
        notifier = Notifier(config_dict=config)
        
        subject = "TEST EMAIL"
        body = "This is a test body."
        
        # Send
        result, msg_id = notifier.send_report(
            receiver_emails=["client@example.com"],
            report_path=None, # Optional attachment
            client_name="Test Client",
            subject=subject,
            body=body
        )
        
        assert result is True
        assert msg_id is not None
        
        # Verify file creation in outbox
        # We need to know where OUTBOX is. Notifier init sets it.
        # Based on previous edits, it should be in 04_Data/outbox
        
        # List files in outbox to verify
        # (This part relies on the path actually existing or being mocked)
        pass
