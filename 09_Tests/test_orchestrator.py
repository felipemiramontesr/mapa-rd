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

    def test_resolve_target_domain(self):
        intake = {"identity": {"domains": ["example.com"], "emails": []}}
        client = {"client_name_slug": "example-co"}
        target = self.orchestrator._resolve_target(intake, client)
        self.assertEqual(target, "example.com")

    def test_resolve_target_email(self):
        intake = {"identity": {"domains": [], "emails": ["user@example.com"]}}
        client = {"client_name_slug": "example-co"}
        target = self.orchestrator._resolve_target(intake, client)
        self.assertEqual(target, "user@example.com")

    def test_resolve_target_slug(self):
        intake = {"identity": {"domains": [], "emails": []}}
        client = {"client_name_slug": "example-co"}
        target = self.orchestrator._resolve_target(intake, client)
        self.assertEqual(target, "example-co")

    @patch('subprocess.run')
    def test_run_spiderfoot_scan_missing_script(self, mock_subprocess):
        # Setup orchestrator with a non-existent path
        self.orchestrator.sf_script = "/non/existent/path/sf.py"
        results = self.orchestrator.run_spiderfoot_scan("target", "scan_id")
        self.assertEqual(results, [])
        mock_subprocess.assert_not_called()

if __name__ == '__main__':
    unittest.main()
