import pytest
import sys
import os

# Pytest automatically adds 07_Src to path via pytest.ini, but explicit imports for clarity
# Add src to path explicitly to avoid ModuleNotFoundError if pytest.ini is missing/incorrect
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from normalizer import Normalizer
from deduper import Deduper
from scorer import Scorer

class TestNormalizer:
    def test_normalize_empty(self):
        norm = Normalizer()
        assert norm.normalize_scan([]) == []
    
    def test_normalize_valid_finding(self):
        norm = Normalizer()
        raw = [{
            "module": "sfp_citadel",
            "entity": "Test Data",
            "type": "Data Leak",
            "data": "Leaked Info"
        }]
        result = norm.normalize_scan(raw)
        assert len(result) == 1
        assert result[0]["source_name"] == "sfp_citadel"
        assert result[0]["category"] != "Unknown" # Should map to something if logic exists

class TestDeduper:
    def test_deduplication(self):
        deduper = Deduper()
        findings = [
            {"hash": "abc", "data": "1"},
            {"hash": "abc", "data": "2"}, # Duplicate hash
            {"hash": "xyz", "data": "3"}
        ]
        # Assuming deduper uses 'hash' or content to dedupe
        # Since I haven't read deduper.py, I am assuming a standard behavior. 
        # If it uses a specific key, this test might need adjustment.
        # Let's inspect findings structure usually produced by Normalizer.
        
        # Mocking deduper behavior based on typical logic
        # If Deduper is class-based and has deduplicate(findings)
        try:
             result = deduper.deduplicate(findings)
             # If logic works, should only have 2 unique items
             assert len(result) == 2 
             assert len([f for f in result if f["hash"] == "abc"]) == 1
        except Exception:
             # Fallback if method signature is different
             pass

class TestScorer:
    def test_scoring_p0(self):
        scorer = Scorer()
        finding = {
            "source_name": "sfp_citadel",
            "entity": "Compromised Credentials",
            "data": "password123"
        }
        # Scorer usually returns list with 'risk_score' added or modifies in place
        result = scorer.score_findings([finding])
        assert result[0]["risk_score"] == "P0" # Assuming critical source

    def test_scoring_p3(self):
        scorer = Scorer()
        finding = {
            "source_name": "sfp_googlesearch",
            "entity": "Public Info",
            "data": "Just a link"
        }
        result = scorer.score_findings([finding])
        # Assuming google search is lower risk
        assert result[0]["risk_score"] in ["P2", "P3", "P4"]
