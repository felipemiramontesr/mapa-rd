import sys
import os
import hashlib

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from deduper import Deduper

# Mock class to simulate pipeline behavior (Normalizer is fine to mock for simple data gen)
class MockNormalizer:
    def normalize_event(self, event):
        etype = event.get("type")
        data = event.get("data")
        unique_str = f"{etype}:{data}"
        fid = hashlib.sha256(unique_str.encode('utf-8')).hexdigest()[:16]
        return {
            "finding_id": fid,
            "event_type": etype,
            "value": data,
            "source_name": event.get("module")
        }

def test_redundancy():
    norm = MockNormalizer()
    dedup = Deduper() # Use REAL Deduper logic
    
    # 1. Exact Duplicates (Should be 1)
    ev1 = {"type": "EMAILADDR", "data": "alice@example.com", "module": "sfp_hunter"}
    ev2 = {"type": "EMAILADDR", "data": "alice@example.com", "module": "sfp_skymem"}
    
    # 2. Cross-Type Redundancy (Should be 1, currently likely 2)
    # Spiderfoot often reports a domain as DOMAIN_NAME and INTERNET_NAME
    ev3 = {"type": "DOMAIN_NAME", "data": "example.com", "module": "sfp_whois"}
    ev4 = {"type": "INTERNET_NAME", "data": "example.com", "module": "sfp_dns"}
    
    findings = [
        norm.normalize_event(ev1), 
        norm.normalize_event(ev2),
        norm.normalize_event(ev3),
        norm.normalize_event(ev4)
    ]
    
    print(f"[*] Raw Findings: {len(findings)}")
    
    results = dedup.deduplicate(findings)
    print(f"[*] Deduped Findings: {len(results)}")
    
    for r in results:
        print(f" - {r['event_type']}: {r['value']} (ID: {r['finding_id']})")

    # EXPECTATION for advanced logic:
    # We want "example.com" to appear ONLY ONCE, regardless of whether it's DOMAIN_NAME or INTERNET_NAME.
    
    has_domain = any(r['event_type'] == 'DOMAIN_NAME' for r in results)
    has_internet = any(r['event_type'] == 'INTERNET_NAME' for r in results)
    
    if has_domain and has_internet:
        print("[FAIL] Redundant domain types found.")
    else:
        print("[PASS] Cross-type redundancy handled (or not present).")

if __name__ == "__main__":
    test_redundancy()
