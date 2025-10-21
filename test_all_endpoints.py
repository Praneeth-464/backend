import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_all_endpoints():
    """
    Test all the new endpoints to ensure they're working properly
    """
    print("Testing all new endpoints...")
    
    # Test pricing endpoint
    print(f"\n[{datetime.now()}] Testing pricing endpoint...")
    fare_request = {
        "origin_lat": 12.9716,
        "origin_lon": 77.5946,
        "destination_lat": 13.0358,
        "destination_lon": 77.5970,
        "rider_beta": 0.7,
        "traffic_multiplier": 1.2
    }
    
    try:
        response = requests.post(f"{BASE_URL}/pricing/estimate", json=fare_request)
        print(f"Pricing Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Pricing endpoint working")
        else:
            print(f"✗ Pricing endpoint failed: {response.json()}")
    except Exception as e:
        print(f"✗ Error testing pricing endpoint: {e}")
    
    # Test analytics endpoint
    print(f"\n[{datetime.now()}] Testing analytics endpoint...")
    try:
        # Use a sample user ID (this would be a real user ID in practice)
        sample_user_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{BASE_URL}/analytics-simple/user/{sample_user_id}")
        print(f"Analytics Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Analytics endpoint working")
        else:
            print(f"✗ Analytics endpoint failed: {response.json()}")
    except Exception as e:
        print(f"✗ Error testing analytics endpoint: {e}")
    
    # Test scheduled rides endpoint
    print(f"\n[{datetime.now()}] Testing scheduled rides endpoint...")
    try:
        # This will fail without a valid rider ID, but we can test the endpoint exists
        sample_rider_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{BASE_URL}/scheduled-rides/rider/{sample_rider_id}")
        print(f"Scheduled Rides Status Code: {response.status_code}")
        if response.status_code in [200, 404]:  # 404 is expected if rider doesn't exist
            print("✓ Scheduled rides endpoint working")
        else:
            print(f"✗ Scheduled rides endpoint failed: {response.json()}")
    except Exception as e:
        print(f"✗ Error testing scheduled rides endpoint: {e}")
    
    # Test wallet endpoint
    print(f"\n[{datetime.now()}] Testing wallet endpoint...")
    try:
        sample_user_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{BASE_URL}/wallet/balance/{sample_user_id}")
        print(f"Wallet Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Wallet endpoint working")
        else:
            print(f"✗ Wallet endpoint failed: {response.json()}")
    except Exception as e:
        print(f"✗ Error testing wallet endpoint: {e}")
    
    # Test loyalty endpoint
    print(f"\n[{datetime.now()}] Testing loyalty endpoint...")
    try:
        sample_user_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{BASE_URL}/loyalty/{sample_user_id}")
        print(f"Loyalty Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Loyalty endpoint working")
        else:
            print(f"✗ Loyalty endpoint failed: {response.json()}")
    except Exception as e:
        print(f"✗ Error testing loyalty endpoint: {e}")
    
    print(f"\n[{datetime.now()}] Endpoint testing complete!")

if __name__ == "__main__":
    test_all_endpoints()