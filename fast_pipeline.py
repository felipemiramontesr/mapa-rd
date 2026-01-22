import sys
import os
import time
from unittest.mock import MagicMock, patch

# Setup paths
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '07_Src'))

from orchestrator import Orchestrator

def run_fast_pipeline():
    print(f"\n{'='*60}")
    print(f" MAPA-RD: FAST PIPELINE EXECUTION (Real Data / No Waiting)")
    print(f"{'='*60}\n")
    
    # Patch the slow SpiderFoot scanner
    # We replace it with a mock that returns a single dummy finding so we know it worked
    with patch('orchestrator.Orchestrator.run_spiderfoot_scan') as mock_sf:
        print("[*] Bypassing legacy SpiderFoot scanner (Save ~10 mins)...")
        mock_sf.return_value = [] 
        
        # Initialize Orchestrator
        orc = Orchestrator()
        
        # Target Client
        client_slug = "Felipe_de_Jesus_Miramontes_Romero"
        print(f"[*] Target Client Slug: {client_slug}")
        
        # We need to find the Intake ID associated with this client or create one on the fly
        # For this test, we'll manually trigger it using the orchestration logic
        
        # 1. Resolve Client ID (or create if missing)
        sm = orc.sm
        client = sm.get_client_by_slug(client_slug)
        if not client:
            print(f"[!] Client not found by slug '{client_slug}', searching by ID 'C001'...")
            client = sm.get_client("C001")
            
        if not client:
            print("[!] CRITICAL: Client 'C001' not found. Creating temporary test client...")
            orc.orchestrate("C001", "TEST_RUN")
            client = sm.get_client("C001")
            
        # FORCE UPDATE for Real OSINT
        print("[*] Updating Client Metadata for OSINT...")
        sm.update_client("C001", 
            client_name_full="Felipe de Jesus Miramontes Romero", 
            email="felipemiramontesr@gmail.com"
        )
        client = sm.get_client("C001") # Reload
            
        client_id = client['id']
        print(f"[*] Identified Client ID: {client_id}")
        
        # 2. Trigger Orchestration (This runs HIBP + DDG for REAL)
        print("[*] Starting Real OSINT Scan (HIBP + DuckDuckGo)...")
        start_time = time.time()
        
        intake_id, _ = orc.orchestrate(client_id, "ON_DEMAND")
        
        elapsed = time.time() - start_time
        print(f"\n[SUCCESS] Pipeline Completed in {elapsed:.2f} seconds.")
        print(f"[*] Report Generated for Intake: {intake_id}")
        
        # 3. Verify Output
        report = sm.data["reports"].get(intake_id) # Report ID is usually same structure or tracked
        # The orchestrator creates a new report ID inside `execute_pipeline`.
        # We can find the latest report for this client.
        
        latest_report = None
        for rid, rdata in sm.data["reports"].items():
            if rdata["client_id"] == client_id:
                latest_report = rdata
                # Keep looping to finding the last one (dict iteration order usually preserves insertion in modern Python)
        
        if latest_report:
            print(f"[*] Latest Report ID: {latest_report['report_id']}")
            print(f"[*] PDF Path: {latest_report['artifacts'].get('final_pdf_path', 'Not found')}")
            
            # Read the JSON findings to show the user REAL DATA
            json_path = latest_report['artifacts'].get('final_pdf_path', '').replace('.html', '.json')
            if os.path.exists(json_path):
                import json
                with open(json_path, 'r', encoding='utf-8') as f:
                    findings = json.load(f)
                
                print(f"\n{'='*30}")
                print(f" REAL FINDINGS SUMMARY ({len(findings)})")
                print(f"{'='*30}")
                
                ddg_count = 0
                hibp_count = 0
                
                for f in findings:
                    if f['finding_id'].startswith("HIBP"):
                        hibp_count += 1
                        print(f"[HIBP] {f['breach_title']}")
                    elif f['finding_id'].startswith("DDG"):
                        ddg_count += 1
                        print(f"[DDG]  {f['title']} ({f['value']})")
                
                if ddg_count == 0:
                    print("[WARN] No DuckDuckGo results found (Rate Limit?).")
                else:
                    print(f"\n[OK] Found {ddg_count} DuckDuckGo results.")
            else:
                print("[!] JSON findings file not found.")

if __name__ == "__main__":
    try:
        run_fast_pipeline()
    except Exception as e:
        input(f"Error: {e}") # Keep window open if crashed
