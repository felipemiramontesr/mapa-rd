
import os
import sys

# Patch paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data_test')
TRACKING_DIR = os.path.join(DATA_DIR, 'tracking')

import state_manager
state_manager.TRACKING_DIR = TRACKING_DIR
state_manager.PERSISTENCE_FILE = os.path.join(TRACKING_DIR, 'persistence.json')

sm = state_manager.StateManager()
sm.reload()

# Create dummy client
cid = sm._get_or_create_client_id("DebugClient")
print(f"Client Created: {cid}")

# Append History
print("Appending history...")
sm.append_report_history(cid, {
    "report_id": "R-9999",
    "type": "BASELINE",
    "status": "ENVIADO"
})

# Verify immediately
print("Verifying in memory...")
client = sm.get_client(cid)
print(f"Reports in memory: {client.get('reports')}")

# Verify Persistence
sm2 = state_manager.StateManager()
sm2.reload()
client2 = sm2.get_client(cid)
print(f"Reports in persistence: {client2.get('reports')}")
