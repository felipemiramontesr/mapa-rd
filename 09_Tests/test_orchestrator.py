import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from orchestrator import Orchestrator

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        # Mock StateManager to avoid file I/O during init
        with patch('state_manager.StateManager') as MockSM:
            self.orchestrator = Orchestrator()
            self.orchestrator.sm = MockSM.return_value

    def test_resolve_target_name(self):
        intake = {"identity": {"emails": []}}
        client = {"client_name_full": "Felipe Miramontes", "client_dir": "C001"}
        target = self.orchestrator._resolve_target(intake, client)
        self.assertEqual(target, "Felipe Miramontes")

    def test_resolve_target_email(self):
        intake = {"identity": {"emails": ["user@example.com"]}}
        client = {"client_name_full": "Test User", "client_dir": "C101"}
        target = self.orchestrator._resolve_target(intake, client)
        self.assertEqual(target, "user@example.com")

    def test_resolve_target_dir(self):
        intake = {"identity": {"emails": []}}
        client = {"client_name_full": "", "client_dir": "example-dir"}
        target = self.orchestrator._resolve_target(intake, client)
        self.assertEqual(target, "example-dir")

    @patch('subprocess.run')
    def test_run_spiderfoot_scan_missing_script(self, mock_subprocess):
        # Setup orchestrator with a non-existent path
        self.orchestrator.sf_script = "/non/existent/path/sf.py"
        results = self.orchestrator.run_spiderfoot_scan("target", "scan_id")
        self.assertEqual(results, [])
        mock_subprocess.assert_not_called()

if __name__ == '__main__':
    unittest.main()
