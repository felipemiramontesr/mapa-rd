import json
import requests
import sys
import os

def load_config():
    config_path = r"c:\Felipe\Projects\Mapa-rd\03_Config\config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def test_google_search():
    config = load_config()
    api_key = config['google_cse']['api_key']
    cx = config['google_cse']['cx']
    
    query = "site:linkedin.com \"seguridad informática\""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}"
    
    print(f"Testing Google API with Key: {api_key[:5]}... and CX: {cx[:5]}...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("SUCCESS: Google API request successful!")
            try:
                data = response.json()
                items = data.get('items', [])
                print(f"Results found: {len(items)}")
                for item in items[:3]:
                    print(f"- {item['title']} ({item['link']})")
                return True
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                return False
        else:
            print(f"ERROR: Google API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_google_search()
