import unittest
import os
import shutil
import tempfile
import sys
import json
from unittest.mock import patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from state_manager import StateManager

class TestStateManager(unittest.TestCase):
    def setUp(self):
        # Create a temp directory for the test state
        self.test_dir = tempfile.mkdtemp()
        self.tracking_dir = os.path.join(self.test_dir, 'tracking')
        self.state_file = os.path.join(self.tracking_dir, 'state.json')
        
        # Initialize StateManager with overridden paths
        # Note: We'll need to monkey-patch or subclass if the paths are hardcoded in __init__
        # Looking at previous file content, paths are set in __init__.
        # We will subclass for testing to override directories easily or just modify the instance attributes
        
        self.sm = StateManager()
        self.sm.TRACKING_DIR = self.tracking_dir
        self.sm.STATE_FILE = self.state_file
        
        # Ensure dir exists as __init__ does
        os.makedirs(self.tracking_dir, exist_ok=True)
        # Reset data for test
        self.sm.data = {
            "clients": {},
            "reports": {},
            "scans": {},
            "intakes": {},
            "logs": []
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_client_creation(self):
        # Test getting an ID
        cid = self.sm._get_or_create_client_id("Test Client")
        self.assertTrue(len(cid) > 0)
        
        # Now creating it explicitly
        self.sm.create_client(cid, "Test Client")
        client = self.sm.get_client(cid)
        self.assertIsNotNone(client)
        self.assertEqual(client['client_name_full'], "Test Client")

    def test_client_idempotency(self):
        # Ensure same name returns same ID
        cid1 = self.sm._get_or_create_client_id("Unique User")
        cid2 = self.sm._get_or_create_client_id("Unique User")
        self.assertEqual(cid1, cid2)

    def test_update_client(self):
        cid = self.sm._get_or_create_client_id("Updater")
        # update_client implicitly creates if missing
        self.sm.update_client(cid, client_name_full="Updater", email="test@example.com", status="ACTIVE")
        
        client = self.sm.get_client(cid)
        self.assertEqual(client['email'], "test@example.com")
        self.assertEqual(client['status'], "ACTIVE")

    def test_persistence(self):
        # We need to patch the global PERSISTENCE_FILE in state_manager module
        with patch('state_manager.PERSISTENCE_FILE', self.state_file):
            # Create a clean SM instance that uses this path? 
            # Actually self.sm uses self.state_manager module's methods
            # so the patch should affect self.sm.save_data()
            
            cid = self.sm._get_or_create_client_id("Persist Me")
            self.sm.update_client(cid, client_name_full="Persist Me", test_val="123")
            
            self.assertTrue(os.path.exists(self.state_file))
            
            # Load new instance to verify read
            sm2 = StateManager()
            sm2._load_data() # Will read from the patched path
            
            client = sm2.get_client(cid)
            # data is loaded into sm2.data
            self.assertIsNotNone(sm2.data["clients"].get(cid))

if __name__ == '__main__':
    unittest.main()
