import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_pricing_functionality():
    """
    Test the pricing and fare estimation functionality
    """
    print("Testing pricing and fare estimation functionality...")
    
    # Test fare estimation
    print(f"\n[{datetime.now()}] Estimating fare...")
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
        print(f"Fare Estimate Status Code: {response.status_code}")
        print(f"Fare Estimate Response: {response.json()}")
    except Exception as e:
        print(f"Error estimating fare: {e}")

if __name__ == "__main__":
    test_pricing_functionality()