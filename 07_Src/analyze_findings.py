import json
from collections import Counter

RAW_FILE = r'data\raw\felipe-de-jesus-miramontes-romero\bb54e9c2-835c-4333-ba92-aaee976062ae\spiderfoot.json'

with open(RAW_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

types = Counter([item.get('type') for item in data])
print("\n--- Event Type Distribution ---")
for t, count in types.most_common():
    print(f"{t}: {count}")

print("\n--- Sample Critical Patterns (Searching for leaks/mentions) ---")
keywords = ["leak", "breach", "password", "banorte", "account", "pwned"]
for item in data:
    content = str(item.get('data', '')).lower()
    for kw in keywords:
        if kw in content:
            print(f"FOUND [{kw}] in Type {item.get('type')}: {item.get('data')[:100]}...")
            break
