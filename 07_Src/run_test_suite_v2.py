import sys
import os
import json
import traceback

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from orchestrator import Orchestrator
from state_manager import StateManager
from client_manager import ClientManager
from report_generator import ReportGenerator

def run_test_suite_v2():
    print(f"\n{'='*60}\nMAPA-RD TEST SUITE v2.3 (FIXED)\n{'='*60}")
    
    # SETUP: Use Test Directory for State
    TEST_TRACKING_DIR = os.path.join(os.getcwd(), 'data_test', 'tracking')
    if not os.path.exists(TEST_TRACKING_DIR):
        os.makedirs(TEST_TRACKING_DIR)
        
    print(f"[INIT] Using Test Persistence: {TEST_TRACKING_DIR}")
    
    # Initialize components pointing to test data if possible, 
    # but StateManager uses global tracking dir by default. 
    # We must patch StateManager's path or instantiate with it if refactored.
    # Since we refactored StateManager to init TRACKING_DIR in __init__, let's hack it 
    # by modifying the class variable or instance variable for this session.
    
    # Clean previous test persistence
    test_persistence = os.path.join(TEST_TRACKING_DIR, 'persistence.json')
    if os.path.exists(test_persistence):
        os.remove(test_persistence)
        
    # Monkey Patching for Test Isolation
    original_tracking_dir = StateManager().TRACKING_DIR # Get default
    
    # We need to ensure all new instances use the test dir.
    # The best way is to subclass or forcing the attribute.
    # Our StateManager is hardcoded to load from module-level TRACKING_DIR in constructor?
    # No, we refactored it to self.TRACKING_DIR = module_level, but module level is hardcoded.
    # Let's overwrite the module level variable if possible, or just overwrite the instance attribute immediately after creation.
    
    # Actually, we can just modify the CONSTANT in the module before instantiation if we import properly.
    import state_manager
    state_manager.TRACKING_DIR = TEST_TRACKING_DIR
    state_manager.PERSISTENCE_FILE = test_persistence
    
    # Re-instantiate to pick up new paths (though our __init__ used the global module var we just patched)
    sm = StateManager() 
    sm.TRACKING_DIR = TEST_TRACKING_DIR # Force it to be sure
    sm.data = { "clients": {}, "reports": {} } # Force clean state
    sm.save_data()
    
    cm = ClientManager()
    cm.state_manager = sm # Inject test SM
    
    rg = ReportGenerator()
    rg.state_manager = sm # Inject test SM
    rg.REPORTS_DIR = os.path.join(os.getcwd(), 'data_test', 'reports') # Isolate reports too
    rg.ARCO_ROOT = os.path.join(os.getcwd(), 'data_test', 'arco')
    rg.ensure_dirs()

    qc_module = rg.QCModule(rg.REPORTS_DIR, rg.ARCO_ROOT)

    client_id = None
    
    # --- TEST A: Client Creation ---
    print("\n[TEST A] Client Creation & Defaults")
    try:
        client_name = "Test_Client_Fix6"
        email = "fix6@test.com"
        client_id = cm.create_client_from_request(client_name, email)
        
        # Verify defaults
        c_state = sm.get_client(client_id)
        assert c_state is not None, "Client State is None"
        assert c_state["incident_count_month"] == 0, "Incident count must be 0"
        assert c_state["last_valid_report"] is None, "Last valid report must be None initially"
        assert c_state["report_seq"] == 0, "Report seq must be 0 initially"
        
        print("[PASS] TEST A: Client Created Successfully with Defaults")
        
    except Exception as e:
        print(f"[FAIL] TEST A CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)

    # --- TEST B: Report Generation (Baseline) & QC ---
    print("\n[TEST B] Baseline Report Generation & QC Flow")
    try:
        sm.set_intake_status(client_id, "AUTORIZADO")
        
        findings = [{"category": "Data Leak", "risk_score": "P0", "entity": "Creds", "source_name": "sfp_citadel"}]
        md_path = rg.generate_report(client_name, findings, report_type="baseline")
        
        sm.reload()
        # Verify Report ID Logic
        base_name = os.path.basename(md_path).replace(".md", "")
        report_info = sm.get_report(base_name)
        
        assert report_info is not None
        assert report_info["qc_status"] == "APROBADO"
        assert report_info["status"] == "ENVIADO"
        
        # Verify Sequence Increment
        c_state = sm.get_client(client_id)
        assert c_state["report_seq"] == 1, f"Report Seq should be 1, got {c_state['report_seq']}"
        assert c_state["last_valid_report"]["report_id"] == "R-0001"
        assert c_state["incident_count_month"] == 0, "Baseline should NOT increment incident count"
        
        print("[PASS] TEST B: Report Generated, QC Passed, Seq Incremented")
        
    except Exception as e:
        print(f"[FAIL] TEST B CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)

    # --- TEST C: Incident Report with Increment ---
    print("\n[TEST C] Incident Report Counter Logic")
    try:
        # Generate INCIDENT report
        md_path_inc = rg.generate_report(client_name, findings, report_type="incident")
        
        sm.reload()
        c_state = sm.get_client(client_id)
        
        assert c_state["report_seq"] == 2, f"Report Seq should be 2, got {c_state['report_seq']}"
        assert c_state["last_valid_report"]["report_id"] == "R-0002"
        # Since it passed QC (default flow in generate_report assumes findings are valid enough unless we broke file), 
        # ID is validated. 
        # Incident Count SHOULD increment
        assert c_state["incident_count_month"] == 1, f"Incident Count should be 1, got {c_state['incident_count_month']}"
        
        print("[PASS] TEST C: Incident Report Correctly Counters")
        
    except Exception as e:
        print(f"[FAIL] TEST C CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    # --- TEST D: Rescue Flow (No Increment) ---
    print("\n[TEST D] Rescue Report Logic")
    try:
        # Rescue report
        md_path_res = rg.generate_report(client_name, findings, report_type="baseline", is_rescue=True)
        
        sm.reload()
        c_state = sm.get_client(client_id)
        
        # Seq increments? Yes, it's a new report file.
        assert c_state["report_seq"] == 3
        # ID should be R-0003
        assert c_state["last_valid_report"]["report_id"] == "R-0003"
        # Incident count should NOT change from previous (1)
        assert c_state["incident_count_month"] == 1, f"Rescue shouldn't increment incident count. Got {c_state['incident_count_month']}"
        
        print("[PASS] TEST D: Rescue Report Handled Correctly")
        
    except Exception as e:
        print(f"[FAIL] TEST D CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)

    # --- FINAL DUMP ---
    print(f"\n{'='*60}\nFINAL PERSISTENCE DUMP (Client {client_id})\n{'='*60}")
    final_client = sm.get_client(client_id)
    print(json.dumps(final_client, indent=4))
    
    print("\nGenerated Files:")
    for f in os.listdir(rg.REPORTS_DIR):
        if client_name in f:
            print(f" - {f}")

if __name__ == "__main__":
    run_test_suite_v2()
