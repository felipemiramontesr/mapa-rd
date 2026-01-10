import json
import os

intake_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '04_Data', 'intake', 'ana-flores.json')

data = {
    "client_id": "ana-flores",
    "intake_type": "ON_DEMAND",
    "requested_by": "Felipe (Admin)",
    "timestamp": "2026-01-09T20:30:00",
    "identity": {
        "names": ["Ana Flores"],
        "emails": ["anafbaca@gmail.com"],
        "domains": [],
        "usernames": []
    },
    "jurisdiction": "MX",
    "modules": ["ALL"]
}

with open(intake_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
    
print(f"Created intake at {intake_path}")
