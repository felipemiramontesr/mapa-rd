import requests
import json
import sys

# Configuration
API_KEY = "344ba3142e664cf29effcebea34e9f3e"
TARGET_EMAIL = "felipemiramontesr@gmail.com"  # Email from your dashboard

def check_my_breaches():
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{TARGET_EMAIL}?truncateResponse=false"
    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "OSINT-Safe-Test"
    }
    
    print(f"\n--- HIBP Safe Test: {TARGET_EMAIL} ---\n")
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            breaches = response.json()
            print(f"SUCCESS: Found {len(breaches)} breaches.")
            print("-" * 50)
            for breach in breaches:
                print(f"* {breach['Name']} ({breach['BreachDate']})")
                print(f"   Classes: {', '.join(breach['DataClasses'][:5])}...")
                print("-" * 50)
            print(f"\nNOTE: This data was fetched directly from the API and NOT saved to any MAPA-RD files.")
        elif response.status_code == 404:
             print("GOOD NEWS: No breaches found for this email.")
        elif response.status_code == 401:
            print("ERROR: Unauthorized. Invalid API Key.")
        else:
            print(f"ERROR: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    check_my_breaches()
