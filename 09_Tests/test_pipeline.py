"""
MAPA-RD: Integrated Pipeline Test Suite
----------------------------------------
Author: Antigravity AI / Senior Python standards
Version: 1.2.0 (Pro)

Purpose:
    Performs a full end-to-end (E2E) validation of the digital intelligence 
    pipeline. This test simulates a client intake, executes a scan, processes 
    data through the entire chain (Normalization -> Scorer -> Resolver), 
    and verifies artifact generation (PDF/Markdown/ARCO).
"""

import sys
import os
import json
import logging
from typing import List

# ---------------------------------------------------------
# DYNAMIC PATH INJECTION
# Adding the source directory to the environment to allow relative imports.
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '07_Src'))

# Core Pipeline Components
from orchestrator import Orchestrator
from normalizer import Normalizer
from deduper import Deduper
from scorer import Scorer
from responsible_resolver import ResponsibleResolver
from arco_generator import ArcoGenerator
from report_generator import ReportGenerator

def test_pipeline() -> None:
    """Full architectural validation of the MAPA-RD intelligence flow."""
    print(f"\n{'='*70}")
    print(" [TEST] STARTING INTEGRATED PIPELINE VALIDATION")
    print(f"{'='*70}\n")
    
    # ---------------------------------------------------------
    # STEP 1: TEST ENVIRONMENT MOCKING
    # We clean and prepare the required data structures for the simulation.
    # ---------------------------------------------------------
    client_id = "test-verification-user"
    orchestrator = Orchestrator()
    
    # Directories for mock data storage
    data_dirs = [
        '04_Data/intake', '04_Data/raw', '04_Data/reports', 
        '04_Data/tracking', '04_Data/outbox'
    ]
    
    for d in data_dirs:
        os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

    # 1.1 Create mock intake record
    mock_intake_path = os.path.join(BASE_DIR, '04_Data', 'intake', f"{client_id}.json")
    with open(mock_intake_path, 'w', encoding='utf-8') as f:
        json.dump({
            "client_id": client_id,
            "identity": {
                "names": ["Felipe Reviewer"],
                "emails": ["felipe@example.com"],
                "domains": ["felipe-demo.com"]
            },
            "jurisdiction": "MX"
        }, f)

    # ---------------------------------------------------------
    # STEP 2: ORCHESTRATION & DATA ACQUISITION
    # ---------------------------------------------------------
    print("[*] Orchestrating scan job...")
    scan_id, client_dir_name = orchestrator.orchestrate(client_id)
    
    # 2.1 Verify raw data persistence
    raw_path = os.path.join(BASE_DIR, '04_Data', 'raw', client_dir_name, scan_id, 'spiderfoot.json')
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Pipeline failed to persist raw data at {raw_path}")

    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # Injected Mock Finding for Report Validation
    raw_data.append({
        "type": "EMAILADDR_COMPROMISED",
        "data": "hack@victim.com",
        "module": "HIBP",
        "confidence": 100
    })
    
    print(f" [+] Raw Intelligence Loaded: {len(raw_data)} events (1 Injected).")

    # ---------------------------------------------------------
    # STEP 3: PROCESSING CHAIN VALIDATION
    # ---------------------------------------------------------
    # 3.1 Normalization (Technical to Human)
    normalizer = Normalizer()
    normalized = normalizer.normalize_scan(raw_data)
    
    # 3.2 Deduplication (Noise Reduction)
    deduped = Deduper().deduplicate(normalized)
    
    # 3.3 Legal Resolution (ARCO Entities)
    resolver = ResponsibleResolver()
    resolved = resolver.resolve_findings(deduped)

    # 3.4 Risk Scoring (Priority Logic)
    scorer = Scorer()
    scored = scorer.score_findings(resolved)
    
    # ---------------------------------------------------------
    # STEP 4: ARTIFACT GENERATION & COMPLIANCE
    # ---------------------------------------------------------
    print("[*] Validating generation of legal & executive artifacts...")
    arco_gen = ArcoGenerator()
    report_gen = ReportGenerator()
    
    # 4.1 ARCO Document Generation
    for finding in scored:
        if finding.get('risk_score') in ['P0', 'P1']:
            path = arco_gen.generate_arco("Felipe Reviewer", finding)
            if not os.path.exists(path):
                raise AssertionError(f"ARCO draft failed to generate at {path}")
            
    # 4.2 Executive Intelligence Report
    artifacts = report_gen.generate_report(client_id, scan_id, "R-AUTO-TC-1", scored, report_type="BASELINE")
    report_path = artifacts["md_path"]
    
    # ---------------------------------------------------------
    # STEP 5: DOCUMENT CONTENT ASSESTMENT
    # Ensuring the markdown contains all required MAPA-RD sections.
    # ---------------------------------------------------------
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    sections = [
        "Alcance", "Escala", "Inventario", "Matriz", "Ruta de Cierre"
    ]
    
    for section in sections:
        assert section in content, f"Compliance Failure: Section '{section}' missing from report."
        print(f" [+] Compliance verified: Section '{section}' found.")

    # ---------------------------------------------------------
    # STEP 6: PDF REPRESENTATION CHECK
    # (Soft check for environment capabilities)
    # ---------------------------------------------------------
    pdf_path = report_path.replace(".md", ".pdf")
    if os.path.exists(pdf_path):
        print(f" [+] PDF Verification: Binary artifact created at {pdf_path}")
    else:
        print(" [!] Note: PDF not found. Skipping binary check (Likely missing Pandoc in this local env).")
        
    print(f"\n{'='*70}")
    print(" [PASSED] PIPELINE VALIDATION COMPLETED SUCCESSFULLY")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # Standard local execution for manual debugging
    test_pipeline()
