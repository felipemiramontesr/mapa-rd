import os
import shutil
import json
import glob

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '04_Data')
TRACKING_FILE = os.path.join(DATA_DIR, 'tracking', 'persistence.json')

CLIENT_slug = "ana-flores"
CLIENT_ID_KEY = "ana-flores" # Based on how we created it

def purge_client():
    print(f"[*] Purging client: {CLIENT_slug}...")
    
    # 1. Remove RAW Data
    raw_path = os.path.join(DATA_DIR, 'raw', CLIENT_slug)
    if os.path.exists(raw_path):
        print(f"    -> Deleting RAW directory: {raw_path}")
        shutil.rmtree(raw_path)
    
    # 2. Remove Reports (match pattern)
    report_pattern = os.path.join(DATA_DIR, 'reports', f"*{CLIENT_slug}*")
    files = glob.glob(report_pattern)
    for f in files:
        print(f"    -> Deleting report artifact: {f}")
        try: os.remove(f)
        except: pass
        
    # 3. Remove Intakes
    intake_pattern = os.path.join(DATA_DIR, 'intake', f"*{CLIENT_slug}*")
    # Also strict match
    intake_strict = os.path.join(DATA_DIR, 'intake', f"{CLIENT_slug}.json")
    
    files = glob.glob(intake_pattern)
    if os.path.exists(intake_strict): files.append(intake_strict)
    
    for f in files:
        print(f"    -> Deleting intake file: {f}")
        try: os.remove(f)
        except: pass
        
    # 4. Clean Persistence JSON (The Brain)
    if os.path.exists(TRACKING_FILE):
        print("    -> Cleaning Persistence JSON...")
        try:
            with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Remove Client
            if CLIENT_ID_KEY in data.get("clients", {}):
                del data["clients"][CLIENT_ID_KEY]
                print(f"    -> Removed client key '{CLIENT_ID_KEY}'")
                
            # Remove related Intakes
            clean_intakes = {}
            for k, v in data.get("intakes", {}).items():
                if v.get("client_id") != CLIENT_ID_KEY:
                    clean_intakes[k] = v
                else:
                    print(f"    -> Removed tracked intake '{k}'")
            data["intakes"] = clean_intakes

            # Remove related Reports
            clean_reports = {}
            for k, v in data.get("reports", {}).items():
                if v.get("client_id") != CLIENT_ID_KEY:
                    clean_reports[k] = v
                else:
                    print(f"    -> Removed tracked report '{k}'")
            data["reports"] = clean_reports
            
            # Save
            with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"[!] Error cleaning persistence: {e}")

    print("[+] Purge Complete.")

if __name__ == "__main__":
    purge_client()
