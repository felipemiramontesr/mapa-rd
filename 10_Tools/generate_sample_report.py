import os
import sys
import json
from datetime import datetime

# Add Src to path
sys.path.append(os.path.join(os.getcwd(), '07_Src'))

from report_generator import ReportGenerator
from state_manager import StateManager

def main():
    print("[-] Verifying clean environment...")
    
    # Files that should NOT exist
    forbidden_files = [
        "04_Data/hibp_mock_anafbaca.json",
        "10_Tools/run_ana_injection.py",
        "08_Templates/report_minimal.html"
    ]
    
    for f in forbidden_files:
        if os.path.exists(f):
            print(f"[!] FAILED: Found forbidden file: {f}")
            return
    print("[+] Cleanup verification passed.")

    print("[-] Generating sample generic report...")
    
    # Output dir
    out_dir = os.path.join("04_Data", "reports")
    os.makedirs(out_dir, exist_ok=True)
    
    # Generic Clean Data
    findings = [
        {
            "risk_score": "P2",
            "breach_title": "Generic Test Breach",
            "breach_date": "2025-01-01",
            "breach_classes": ["Email addresses", "Passwords"],
            "description": "This is a generated test finding to verify the report system works without mocks."
        }
    ]
    
    # Generate
    rg = ReportGenerator()
    result = rg.generate_report(
        client_name="Test Client",
        report_id="REP-TEST-001",
        client_id="test-client-id",
        findings=findings
    )
    
    print(f"[+] Report generated successfully at: {result['pdf_path']}")

if __name__ == "__main__":
    main()
