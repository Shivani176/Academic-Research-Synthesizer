# test_token.py - Simple test to verify your Hugging Face token works

import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_huggingface_token():
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    
    if not token:
        print("❌ No HUGGINGFACE_API_TOKEN found in .env file")
        return False
    
    print(f"✓ Token found: {token[:10]}...{token[-5:]}")
    
    # Test with a simple API call
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try a simple model that should work
    api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
    data = {"inputs": "Hello, how are you?"}
    
    try:
        print("Testing API connection...")
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! API is working")
            print(f"Response: {result}")
            return True
        elif response.status_code == 401:
            print("❌ AUTHENTICATION ERROR: Invalid token")
            return False
        elif response.status_code == 429:
            print("⚠️ RATE LIMITED: Too many requests")
            print("Your token works, but you've hit the rate limit")
            return True
        else:
            print(f"⚠️ API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Hugging Face Token...")
    print("=" * 40)
    
    if test_huggingface_token():
        print("✅ Your token is working! You can proceed with the main script.")
    else:
        print("❌ Token test failed. Please check your token and try again.")
        print("\nTroubleshooting:")
        print("1. Go to https://huggingface.co/settings/tokens")
        print("2. Create a new token with 'Read' permissions")  
        print("3. Copy it to your .env file as HUGGINGFACE_API_TOKEN=hf_your_token")