import requests
import json
from datetime import datetime
from uuid import UUID

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_rider_endpoints():
    """
    Test the new rider endpoints for mobile app functionality
    """
    print("Testing rider endpoints for mobile app...")
    
    # First, let's create a rider
    print(f"\n[{datetime.now()}] Creating a new rider...")
    rider_data = {
        "name": "Mobile App Rider",
        "email": "mobile.rider@example.com",
        "origin_lat": 12.9716,
        "origin_lon": 77.5946,
        "destination_lat": 13.0358,
        "destination_lon": 77.5970,
        "preferred_departure": "2025-10-16T08:30:00+05:30",
        "preferred_arrival": "2025-10-16T09:00:00+05:30",
        "beta": 0.7
    }
    
    try:
        response = requests.post(f"{BASE_URL}/riders/request", json=rider_data)
        print(f"Create Rider Status Code: {response.status_code}")
        rider_response = response.json()
        print(f"Create Rider Response: {rider_response}")
        
        if response.status_code != 200:
            print("Failed to create rider. Exiting test.")
            return
            
        rider_id = rider_response["id"]
        print(f"Created rider with ID: {rider_id}")
        
    except Exception as e:
        print(f"Error creating rider: {e}")
        return
    
    # Test getting rider details
    print(f"\n[{datetime.now()}] Getting rider details...")
    try:
        response = requests.get(f"{BASE_URL}/riders/{rider_id}")
        print(f"Get Rider Status Code: {response.status_code}")
        print(f"Get Rider Response: {response.json()}")
    except Exception as e:
        print(f"Error getting rider: {e}")
    
    # Test updating rider details
    print(f"\n[{datetime.now()}] Updating rider details...")
    updated_rider_data = rider_data.copy()
    updated_rider_data["beta"] = 0.8  # Updated patience factor
    
    try:
        response = requests.put(f"{BASE_URL}/riders/{rider_id}", json=updated_rider_data)
        print(f"Update Rider Status Code: {response.status_code}")
        print(f"Update Rider Response: {response.json()}")
    except Exception as e:
        print(f"Error updating rider: {e}")
    
    # Test getting rider ride history (should be empty initially)
    print(f"\n[{datetime.now()}] Getting rider ride history...")
    try:
        response = requests.get(f"{BASE_URL}/riders/{rider_id}/rides")
        print(f"Get Ride History Status Code: {response.status_code}")
        print(f"Get Ride History Response: {response.json()}")
    except Exception as e:
        print(f"Error getting ride history: {e}")
    
    # Test getting rider notifications (should be empty initially)
    print(f"\n[{datetime.now()}] Getting rider notifications...")
    try:
        response = requests.get(f"{BASE_URL}/riders/{rider_id}/notifications")
        print(f"Get Notifications Status Code: {response.status_code}")
        print(f"Get Notifications Response: {response.json()}")
    except Exception as e:
        print(f"Error getting notifications: {e}")
    
    # Test listing all riders
    print(f"\n[{datetime.now()}] Listing all riders...")
    try:
        response = requests.get(f"{BASE_URL}/riders/")
        print(f"List Riders Status Code: {response.status_code}")
        print(f"List Riders Response: {response.json()}")
    except Exception as e:
        print(f"Error listing riders: {e}")

if __name__ == "__main__":
    test_rider_endpoints()