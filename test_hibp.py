import requests
import json
import sys

def check_hibp(api_key):
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com"
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "OSINT-Test-Script"
    }
    
    print(f"Testing HIBP API Key: {api_key[:4]}...{api_key[-4:]}")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("SUCCESS: HIBP API Key is valid.")
            print(f"Breaches found for test@example.com: {len(response.json())}")
            return True
        elif response.status_code == 401:
            print("ERROR: Unauthorized. Invalid API Key.")
            return False
        else:
            print(f"ERROR: Unexpected status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    check_hibp("344ba3142e664cf29effcebea34e9f3e")
