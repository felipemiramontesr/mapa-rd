import json
import hashlib
from datetime import datetime

class Normalizer:
    def __init__(self):
        pass

    def normalize_event(self, sf_event):
        """
        Transforms a single SF event into MAPA-RD schema with high-fidelity mapping.
        """
        event_type = sf_event.get("type", sf_event.get("event_type", "Unknown"))
        data = sf_event.get("data", "")
        # SF sometimes puts the module name in 'module' or we infer it
        module = sf_event.get("module", "Internal")
        
        # Mapping Dictionary for high-fidelity categorization
        mapa_map = {
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

        # Fallback for Malicious/Blacklisted patterns
        if "MALICIOUS" in event_type:
            category, entity = ("Threat", "Malicious Association")
        elif "BLACKLISTED" in event_type:
            category, entity = ("Threat", "Blacklisted Association")
        elif event_type in mapa_map:
            category, entity = mapa_map[event_type]
        else:
            category, entity = ("Footprint", event_type.replace("_", " ").title())

        # Generate Finding ID (Deterministic Hash)
        unique_str = f"{event_type}{data}"
        finding_id = hashlib.sha256(unique_str.encode('utf-8')).hexdigest()

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

    def normalize_scan(self, raw_data):
        normalized_list = []
        for event in raw_data:
            normalized_list.append(self.normalize_event(event))
        return normalized_list
