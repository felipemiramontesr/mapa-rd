import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '07_Src'))

from orchestrator import Orchestrator

class TestDDGIntegration(unittest.TestCase):
    @patch('orchestrator.Orchestrator.run_spiderfoot_scan')
    @patch('orchestrator.Orchestrator.run_hibp_scan')
    def test_pipeline_with_ddg(self, mock_hibp, mock_sf):
        # Setup Mocks
        mock_sf.return_value = [] # Skip SF
        mock_hibp.return_value = [] # Skip HIBP
        
        # Init
        orc = Orchestrator()
        
        # Test DDG Direct Call
        print("\n[*] Testing DDG Module directly via Orchestrator...")
        # Use a generic query to guarantee results for integration verification
        results = orc.run_osint_scan("python programming")
        
        print(f"[+] DDG returned {len(results)} findings.")
        self.assertTrue(len(results) > 0, "DDG should return results for this target")
        self.assertEqual(results[0]['category'], "Web Mention")
        print(f"   - First result: {results[0]['title']}")

if __name__ == '__main__':
    unittest.main()
