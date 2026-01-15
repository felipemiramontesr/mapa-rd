
import re

file_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all VEC-XXX IDs
ids = re.findall(r'<div class="vector-id">(VEC-\d+)</div>', content)

print(f"Total Vectors Found: {len(ids)}")
unique_ids = set(ids)
print(f"Unique Vectors: {len(unique_ids)}")

from collections import Counter
counts = Counter(ids)

duplicates = [item for item, count in counts.items() if count > 1]
print(f"Duplicates: {duplicates}")

if duplicates:
    print("WARNING: Duplicate cards detected. This explains the vertical scrolling.")
else:
    print("No duplicates found by ID.")
