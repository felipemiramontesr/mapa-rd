import sqlite3
import json
import os
from datetime import datetime

# Path to SpiderFoot DB
DB_PATH = r'C:\Users\felip\.\spiderfoot\spiderfoot.db'
if not os.path.exists(DB_PATH):
    # Fallback to home dir
    DB_PATH = os.path.expanduser('~/.spiderfoot/spiderfoot.db')

# Mapping for specific client targets (last 24-48h)
TARGETS = [
    'felipemiramontesr.net',
    'private.felipemiramontesr.net',
    'ana.felipemiramontesr.net',
    'felipemiramontesr@gmail.com',
    'info@felipemiramontesr.net',
    'felipemiramontesr',
    'Felipe Miramontes',
    '+524481117977',
    'Dreamtek'
]

def rescue_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get scans for these targets from the last 2 days
    # started is in milliseconds
    threshold = (datetime.now().timestamp() - 172800) * 1000 
    
    query = """
    SELECT r.type, r.data, r.module, r.generated, r.source_event_hash
    FROM tbl_scan_results r
    JOIN tbl_scan_instance i ON r.scan_instance_id = i.guid
    WHERE i.started > ? 
    AND (i.seed_target IN ({seq}))
    """.format(seq=','.join(['?']*len(TARGETS)))
    
    cursor.execute(query, [threshold] + TARGETS)
    rows = cursor.fetchall()
    
    results = []
    for row in rows:
        results.append({
            "type": row[0],
            "data": row[1],
            "module": row[2],
            "generated": row[3],
            "source": row[4]
        })
    
    conn.close()
    
    output_path = r'c:\Users\felip\OneDrive\Documentos\felipe\02_Proyectos_y_Clientes\Mapa-rd\data\raw\felipe-de-jesus-miramontes-romero\bb54e9c2-835c-4333-ba92-aaee976062ae\spiderfoot.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"[+] Successfully rescued {len(results)} events to {output_path}")

if __name__ == "__main__":
    rescue_data()
