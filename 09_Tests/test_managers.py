import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from client_manager import ClientManager
from qc_manager import QCManager
from config_manager import ConfigManager

class TestClientManager(unittest.TestCase):
    def setUp(self):
        self.cm = ClientManager()
        # Mock the internal state manager
        self.cm.state_manager = MagicMock()
        # Fix: Provide a real path string for TRACKING_DIR so os.path.join works
        import tempfile
        self.test_dir = tempfile.mkdtemp()
        self.cm.state_manager.TRACKING_DIR = self.test_dir
        self.cm.state_manager.sanitize_filename.return_value = "safe_name"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
        
    def test_create_client(self):
        # Mocking registry to avoid disk usage
        self.cm.registry = {"next_global_client_id": 101, "clients": {}}
        with patch.object(self.cm, '_save_registry'):
            cid = self.cm.create_client("Juan Perez", "juan@test.com")
            self.assertEqual(cid, "C101")

class TestQCManager(unittest.TestCase):
    def setUp(self):
        self.mock_sm = MagicMock()
        self.qcm = QCManager(self.mock_sm)
        
    def test_filename_validation_valid(self):
        # "MAPA-RD - DATOS_CLIENTE - 123456 - Felipe - C-0001 - 2026-01-01" check regex
        # Pattern: ^MAPA-RD - (TYPE) - (\d+) - ([A-Za-z0-9_-]+) - (R-[0-9A-Za-z-]+|I-[0-9A-Za-z-]+) - (\d{4}-\d{2}-\d{2})$
        # Adjusting test case to match expected standard
        valid_name = "MAPA-RD - REPORTE - 1001 - Cliente_A - R-001 - 2026-01-01.pdf"
        is_valid, _ = self.qcm.validate_filename(valid_name)
        self.assertTrue(is_valid)

    def test_filename_validation_invalid(self):
        invalid_name = "Reporte_Final.pdf"
        is_valid, msg = self.qcm.validate_filename(invalid_name)
        self.assertFalse(is_valid)
        self.assertIn("violates", msg)

class TestConfigManager(unittest.TestCase):
    def test_singleton(self):
        c1 = ConfigManager()
        c2 = ConfigManager()
        self.assertIs(c1, c2)
        
    def test_get_value(self):
        cm = ConfigManager()
        # Assuming config.json has default values or we can mock _load_config
        # But we can test safe get
        val = cm.get("non_existent_key", "default_val")
        self.assertEqual(val, "default_val")

if __name__ == '__main__':
    unittest.main()
