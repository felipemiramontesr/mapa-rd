import json
import os

intake_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '04_Data', 'intake', 'generic_intake.json')

data = {
    "client_id": "client-id-placeholder",
    "intake_type": "ON_DEMAND",
    "requested_by": "System User",
    "timestamp": "2026-01-01T00:00:00",
    "identity": {
        "names": ["Client Name"],
        "emails": ["client@example.com"],
        "domains": ["example.com"],
        "usernames": []
    },
    "jurisdiction": "MX",
    "modules": ["ALL"]
}

with open(intake_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
    
print(f"Created intake at {intake_path}")
