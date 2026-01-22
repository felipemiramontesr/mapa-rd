from duckduckgo_search import DDGS
import logging
import time

# Set up verbose logging
logging.basicConfig(level=logging.DEBUG)

print("=== VERIFICACIÓN DE DATOS REALES (DUCKDUCKGO) ===")
queries = [
    "Felipe de Jesus Miramontes Romero",
    '"Mapa-rd" cyber',
    "site:linkedin.com Felipe de Jesus Miramontes Romero"
]

with DDGS() as ddgs:
    for q in queries:
        print(f"\n[*] Buscando: '{q}' ...")
        try:
            # Try to fetch 3 results
            results = list(ddgs.text(q, max_results=3))
            
            if results:
                print(f"[SUCCESS] Se encontraron {len(results)} resultados reales:")
                for r in results:
                    print(f"  > Título: {r.get('title')}")
                    print(f"    Link: {r.get('href')}")
            else:
                print(f"[WARNING] 0 resultados. ¿Bloqueo o simplemente no hay data?")
                
        except Exception as e:
            print(f"[ERROR] Falló la búsqueda: {e}")
        
        # Respectful pause to avoid ban
        time.sleep(2)
