import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from normalizer import Normalizer
from scorer import Scorer
from report_generator import ReportGenerator

def process_rescue():
    RAW_FILE = r'data\raw\felipe-de-jesus-miramontes-romero\bb54e9c2-835c-4333-ba92-aaee976062ae\spiderfoot.json'
    
    if not os.path.exists(RAW_FILE):
        print(f"[!] Raw file not found: {RAW_FILE}")
        return

    print("[*] Loading raw data...")
    with open(RAW_FILE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f"[*] Normalizing {len(raw_data)} events...")
    norm = Normalizer().normalize_scan(raw_data)
    
    print("[*] Scoring findings...")
    scored = Scorer().score_findings(norm)
    
    client_name = 'Felipe de Jesús Miramontes Romero'
    
    print(f"[*] Generating report for {client_name} (RESCUE BASELINE)...")
    ReportGenerator().generate_report(client_name, scored, report_type='baseline', is_rescue=True)
    
    print(f"[+] Final Re-generated Report and technical annex saved in data/reports/")

if __name__ == "__main__":
    process_rescue()
