import hashlib
from datetime import datetime
from typing import List, Dict, Any, Tuple

class Normalizer:
    """Transforms raw SpiderFoot findings into the unified MAPA-RD data schema.
    
    This class handles the mapping of technical event types to human-readable
    categories and ensures data consistency across the pipeline.
    """

    # High-fidelity categorization map for MAPA-RD indicators
    INDICATOR_MAP: Dict[str, Tuple[str, str]] = {
        "EMAILADDR": ("Contact", "Email"),
        "PHONE_NUMBER": ("Contact", "Phone"),
        "PHYSICAL_ADDRESS": ("Contact", "Address"),
        "EMAILADDR_COMPROMISED": ("Data Leak", "Compromised Credentials"),
        "ACCOUNT_EXTERNAL_OWNED": ("Social Footprint", "External Account"),
        "HUMAN_NAME": ("Identity", "Full Name"),
        "USERNAME": ("Identity", "Handle/User"),
        "DOMAIN_NAME": ("Identity", "Domain"),
        "INTERNET_NAME": ("Identity", "Host/Subdomain"),
        "MALICIOUS_IPADDR": ("Threat", "Malicious IP"),
        "MALICIOUS_AFFILIATE_IPADDR": ("Threat", "Malicious Host"),
        "BLACKLISTED_IPADDR": ("Threat", "Blacklisted IP"),
        "INTERESTING_FILE": ("Data Leak", "Sensitive File Exposed"),
        "RAW_FILE_META_DATA": ("Data Leak", "Document Metadata"),
        "SIMILARDOMAIN": ("Identity", "Squatted/Similar Domain")
    }

    def normalize_event(self, sf_event: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single SpiderFoot event into a standardized MAPA-RD finding.
        
        Args:
            sf_event: The raw event dictionary from SpiderFoot output.
            
        Returns:
            A normalized dictionary containing finding_id, entity, category, etc.
        """
        event_type = sf_event.get("type", sf_event.get("event_type", "Unknown"))
        data = sf_event.get("data", "")
        module = sf_event.get("module", "Internal")
        
        # 1. Resolve Category and Entity Label
        if "MALICIOUS" in event_type:
            category, entity = ("Threat", "Malicious Association")
        elif "BLACKLISTED" in event_type:
            category, entity = ("Threat", "Blacklisted Association")
        elif event_type in self.INDICATOR_MAP:
            category, entity = self.INDICATOR_MAP[event_type]
        else:
            category, entity = ("Footprint", event_type.replace("_", " ").title())

        # 2. Generate Deterministic Finding ID (Collision avoidance)
        unique_str = f"{event_type}:{data}"
        finding_id = hashlib.sha256(unique_str.encode('utf-8')).hexdigest()[:16]

        return {
            "finding_id": finding_id,
            "entity": entity,
            "value": data,
            "category": category,
            "source_name": module,
            "event_type": event_type,
            "url": sf_event.get("url", "N/A"),
            "confidence": sf_event.get("confidence", 100) / 100.0,
            "captured_at": datetime.now().isoformat(),
            "evidence": {
                "raw_type": event_type,
                "module": module
            }
        }

    def normalize_scan(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize a batch of SpiderFoot events.
        
        Args:
            raw_data: List of raw SpiderFoot result dictionaries.
            
        Returns:
            A list of normalized MAPA-RD findings.
        """
        return [self.normalize_event(event) for event in raw_data if event]
