import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import shutil
import tempfile

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        # use a temp dir for reports to avoid cluttering real folders
        self.test_dir = tempfile.mkdtemp()
        
        with patch('state_manager.StateManager'):
            self.rg = ReportGenerator()
            # Override paths to use temp dir
            self.rg.reports_dir = self.test_dir
            self.rg.ensure_dirs()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_sanitize_filename(self):
        name = "Ana Flores (Test)"
        sanitized = self.rg.sanitize_filename(name)
        self.assertEqual(sanitized, "Ana_Flores_(Test)") # Simple replace space with _

        name_accents = "Canción"
        sanitized = self.rg.sanitize_filename(name_accents)
        self.assertEqual(sanitized, "Cancion")

    def test_build_report_name(self):
        name = self.rg._build_report_name("REPORTE", "cli-01", "Client Name", "REP-005", "2025-10-10")
        self.assertEqual(name, "MAPA-RD_cli-01_Client_Name_10102025_005")

    def test_generate_report_structure(self):
        findings = [{"risk_score": "P2", "breach_title": "Test"}]
        result = self.rg.generate_report(
            client_name="Test Client", 
            report_id="R-TEST", 
            client_id="t-client", 
            findings=findings
        )
        
        self.assertTrue(os.path.exists(result["pdf_path"])) # It returns html path as pdf_path key currently
        self.assertTrue(result["pdf_path"].endswith(".html"))

if __name__ == '__main__':
    unittest.main()
