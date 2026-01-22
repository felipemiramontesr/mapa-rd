import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '07_Src'))

from duck_search import DuckSearch

def diag_duck():
    print("=== MAPA-RD: DuckDuckGo OSINT Diagnostic ===")
    ds = DuckSearch()
    target = "felipemiramontesr@gmail.com"
    print(f"[*] Querying for: {target}")
    
    results = ds.search(target)
    
    if not results:
        print("[!] No results found (or error occurred).")
        return
        
    print(f"[+] Found {len(results)} results:")
    for i, r in enumerate(results):
        print(f"\n[{i+1}] {r['title']}")
        print(f"    Link: {r['value']}")
        print(f"    Snippet: {r['snippet'][:100]}...")

if __name__ == "__main__":
    diag_duck()
