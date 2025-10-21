import requests
import json
from datetime import datetime
from uuid import UUID

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_loyalty_functionality():
    """
    Test the loyalty program functionality
    """
    print("Testing loyalty program functionality...")
    
    # You'll need a valid user ID
    print(f"\n[{datetime.now()}] You'll need a valid user ID to test loyalty functionality.")
    user_id = input("Enter a valid user ID: ")
    
    # Test getting loyalty info
    print(f"\n[{datetime.now()}] Getting loyalty info...")
    try:
        response = requests.get(f"{BASE_URL}/loyalty/{user_id}")
        print(f"Get Loyalty Info Status Code: {response.status_code}")
        print(f"Get Loyalty Info Response: {response.json()}")
    except Exception as e:
        print(f"Error getting loyalty info: {e}")
    
    # Test adding loyalty points
    print(f"\n[{datetime.now()}] Adding loyalty points...")
    try:
        response = requests.post(f"{BASE_URL}/loyalty/points", json={"user_id": user_id, "points": 50})
        print(f"Add Points Status Code: {response.status_code}")
        print(f"Add Points Response: {response.json()}")
    except Exception as e:
        print(f"Error adding loyalty points: {e}")
    
    # Test subtracting loyalty points
    print(f"\n[{datetime.now()}] Subtracting loyalty points...")
    try:
        response = requests.post(f"{BASE_URL}/loyalty/points", json={"user_id": user_id, "points": -20})
        print(f"Subtract Points Status Code: {response.status_code}")
        print(f"Subtract Points Response: {response.json()}")
    except Exception as e:
        print(f"Error subtracting loyalty points: {e}")

if __name__ == "__main__":
    test_loyalty_functionality()