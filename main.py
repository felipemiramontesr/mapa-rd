import os
import sys
import argparse
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '07_Src'))

from orchestrator import Orchestrator
from normalizer import Normalizer
from deduper import Deduper
from scorer import Scorer
from responsible_resolver import ResponsibleResolver
from arco_generator import ArcoGenerator
from report_generator import ReportGenerator
from notifier import Notifier

def run_production_pipeline(client_id, analysis_type="monthly"):
    # 1. Initialization and Data Loading
    orchestrator = Orchestrator()
    normalizer = Normalizer()
    deduper = Deduper()
    scorer = Scorer()
    resolver = ResponsibleResolver()
    report_gen = ReportGenerator()

    # Mapping backward compatibility
    if analysis_type == "SETUP":
        analysis_type = "baseline"
    elif analysis_type == "MONTHLY":
        analysis_type = "monthly"

    # Load intake data to get the professional name
    intake_path = os.path.join('04_Data', 'intake', f"{client_id}.json")
    if not os.path.exists(intake_path):
        print(f"[!] Error: Intake file not found at {intake_path}")
        return

    with open(intake_path, 'r', encoding='utf-8') as f:
        intake_data = json.load(f)
    
    full_client_name = intake_data.get('client_info', {}).get('name', client_id)

    print(f"\n{'='*60}")
    print(f" MAPA-RD EXECUTION: {full_client_name}")
    print(f"{'='*60}\n")

    try:
        # 2. Orchestration (Scanning/Data Collection)
        print(f"[*] Step 1: Orchestrating data collection for {client_id}...")
        scan_id, client_dir_name = orchestrator.orchestrate(client_id, analysis_type=analysis_type)
        
        # 3. Load and Process Data
        raw_path = os.path.join('04_Data', 'raw', client_dir_name, scan_id, 'spiderfoot.json')
        
        if not os.path.exists(raw_path):
            print(f"[!] Error: Raw data for scan {scan_id} not found at {raw_path}")
            return

        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # 4. Processing Chain
        print("[*] Step 2: Normalizing and Deduping findings...")
        normalized = normalizer.normalize_scan(raw_data)
        deduped = deduper.deduplicate(normalized)
        
        print("[*] Step 3: Resolving responsibles and Scoring risk...")
        resolved = resolver.resolve_findings(deduped)
        scored = scorer.score_findings(resolved)

        # 5. Reporting
        print("[*] Step 4: Generating Premium PDF Report...")
        # Use full name for internal report content
        report_path = report_gen.generate_report(full_client_name, scan_id, scored, report_type=analysis_type)
        
        pdf_path = report_path.replace(".md", ".pdf")
        
        print(f"\n{'-'*60}")
        print(f"[SUCCESS] Pipeline completed.")
        print(f"  - Markdown: {report_path}")
        print(f"  - Final PDF: {pdf_path}")
        print(f"{'-'*60}\n")

        # 6. Notification
        print("[*] Step 5: Sending Email Notifications...")
        try:
            notifier = Notifier()
            recipients = []
            client_email = intake_data.get('client_info', {}).get('email')
            if client_email:
                recipients.append(client_email)
            
            # Add identity emails too
            identity_emails = intake_data.get('identity', {}).get('emails', [])
            for em in identity_emails:
                if em not in recipients:
                    recipients.append(em)
            
            if recipients:
                # Passing scan_id to notifier so it can extract the report number
                notifier.send_report(recipients, pdf_path, full_client_name, scan_id=scan_id)
            else:
                print("[!] No recipient emails found in intake file.")
        except Exception as e:
            print(f"[!] Notification step failed: {e}")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Pipeline failed: {str(e)}")
        print("Please verify the intake file exists in 'data/intake/'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MAPA-RD Production Pipeline")
    parser.add_argument("--client", required=True, help="Client name (matches intake filename)")
    parser.add_argument("--type", choices=["baseline", "monthly", "on_demand", "incident", "SETUP", "MONTHLY"], default="monthly", help="Analysis type")
    
    args = parser.parse_args()
    
    # Ensure directories exist
    os.makedirs('data/intake', exist_ok=True)
    os.makedirs('data/reports', exist_ok=True)
    
    run_production_pipeline(args.client, args.type)
