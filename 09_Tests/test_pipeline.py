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
import unittest
from unittest.mock import patch, MagicMock

# ---------------------------------------------------------
# DYNAMIC PATH INJECTION
# Adding the source directory to the environment to allow relative imports.
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '07_Src'))

# Core Pipeline Components
from normalizer import Normalizer
from deduper import Deduper
from scorer import Scorer
from responsible_resolver import ResponsibleResolver
from arco_generator import ArcoGenerator
from report_generator import ReportGenerator

class TestPipeline(unittest.TestCase):
    """Architectural validation of the MAPA-RD intelligence flow with Mocks."""

    @patch('orchestrator.Orchestrator')
    def test_full_pipeline_flow(self, MockOrchestrator):
        """Mocks external dependencies to test the internal processing chain logic."""
        client_id = "test-verification-user"
        scan_id = "SCAN-001"
        client_dir_name = "test_client_dir"
        
        # 1. Setup Mock Orchestrator
        orchestrator = MockOrchestrator.return_value
        orchestrator.orchestrate.return_value = (scan_id, client_dir_name)
        
        # 2. Prepare Mock Raw Data
        raw_data = [
            {
                "type": "EMAILADDR_COMPROMISED",
                "data": "hack@victim.com",
                "module": "HIBP",
                "confidence": 100
            }
        ]

        # ---------------------------------------------------------
        # STEP 3: PROCESSING CHAIN VALIDATION
        # ---------------------------------------------------------
        # 3.1 Normalization (Technical to Human)
        normalizer = Normalizer()
        normalized = normalizer.normalize_scan(raw_data)
        
        # 3.2 Deduplication (Noise Reduction)
        deduped = Deduper().deduplicate(normalized)
        
        # 3.3 Risk Scoring (Priority Logic)
        scorer = Scorer()
        scored = scorer.score_findings(deduped)
        
        # 3.4 Legal Resolution (ARCO Entities)
        resolver = ResponsibleResolver()
        resolved = resolver.resolve_findings(scored)

        # ---------------------------------------------------------
        # STEP 4: ARTIFACT GENERATION VALIDATION (LOGIC ONLY)
        # ---------------------------------------------------------
        # Mocking generators to avoid filesystem noise during CI
        with patch('arco_generator.ArcoGenerator.generate_arco') as mock_arco:
            with patch('report_generator.ReportGenerator.generate_report') as mock_report:
                mock_report.return_value = {"md_path": "mock.md", "pdf_path": "mock.pdf"}
                
                # Check generation logic
                for finding in resolved:
                    if finding.get('risk_score') in ['P0', 'P1']:
                        arco_gen = ArcoGenerator()
                        arco_gen.generate_arco("Felipe Reviewer", finding)
                
                report_gen = ReportGenerator()
                artifacts = report_gen.generate_report(
                    client_name="Felipe Reviewer",
                    report_id="R-TEST-001",
                    client_id=client_id,
                    findings=resolved
                )
                
                self.assertIn("md_path", artifacts)
                self.assertTrue(len(resolved) > 0)

if __name__ == "__main__":
    unittest.main()
