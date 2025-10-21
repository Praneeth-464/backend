import requests
import json
from datetime import datetime
from uuid import UUID

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_driver_endpoints():
    """
    Test the new driver endpoints for mobile app functionality
    """
    print("Testing driver endpoints for mobile app...")
    
    # First, let's create a driver
    print(f"\n[{datetime.now()}] Creating a new driver...")
    driver_data = {
        "name": "Mobile App Driver",
        "email": "mobile.driver@example.com",
        "current_lat": 12.9716,
        "current_lon": 77.5946,
        "available": True,
        "rating": 4.8
    }
    
    try:
        response = requests.post(f"{BASE_URL}/drivers/", json=driver_data)
        print(f"Create Driver Status Code: {response.status_code}")
        driver_response = response.json()
        print(f"Create Driver Response: {driver_response}")
        
        if response.status_code != 200:
            print("Failed to create driver. Exiting test.")
            return
            
        driver_id = driver_response["id"]
        print(f"Created driver with ID: {driver_id}")
        
    except Exception as e:
        print(f"Error creating driver: {e}")
        return
    
    # Test getting driver details
    print(f"\n[{datetime.now()}] Getting driver details...")
    try:
        response = requests.get(f"{BASE_URL}/drivers/{driver_id}")
        print(f"Get Driver Status Code: {response.status_code}")
        print(f"Get Driver Response: {response.json()}")
    except Exception as e:
        print(f"Error getting driver: {e}")
    
    # Test updating driver details
    print(f"\n[{datetime.now()}] Updating driver details...")
    updated_driver_data = driver_data.copy()
    updated_driver_data["rating"] = 4.9  # Updated rating
    
    try:
        response = requests.put(f"{BASE_URL}/drivers/{driver_id}", json=updated_driver_data)
        print(f"Update Driver Status Code: {response.status_code}")
        print(f"Update Driver Response: {response.json()}")
    except Exception as e:
        print(f"Error updating driver: {e}")
    
    # Test updating driver location
    print(f"\n[{datetime.now()}] Updating driver location...")
    location_data = {
        "current_lat": 13.0358,
        "current_lon": 77.5970,
        "available": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/drivers/{driver_id}/location", json=location_data)
        print(f"Update Location Status Code: {response.status_code}")
        print(f"Update Location Response: {response.json()}")
    except Exception as e:
        print(f"Error updating location: {e}")
    
    # Test getting driver ride history (should be empty initially)
    print(f"\n[{datetime.now()}] Getting driver ride history...")
    try:
        response = requests.get(f"{BASE_URL}/drivers/{driver_id}/rides")
        print(f"Get Ride History Status Code: {response.status_code}")
        print(f"Get Ride History Response: {response.json()}")
    except Exception as e:
        print(f"Error getting ride history: {e}")
    
    # Test getting driver earnings
    print(f"\n[{datetime.now()}] Getting driver earnings...")
    try:
        response = requests.get(f"{BASE_URL}/drivers/{driver_id}/earnings")
        print(f"Get Earnings Status Code: {response.status_code}")
        print(f"Get Earnings Response: {response.json()}")
    except Exception as e:
        print(f"Error getting earnings: {e}")
    
    # Test getting driver ratings
    print(f"\n[{datetime.now()}] Getting driver ratings...")
    try:
        response = requests.get(f"{BASE_URL}/drivers/{driver_id}/ratings")
        print(f"Get Ratings Status Code: {response.status_code}")
        print(f"Get Ratings Response: {response.json()}")
    except Exception as e:
        print(f"Error getting ratings: {e}")
    
    # Test getting driver notifications (should be empty initially)
    print(f"\n[{datetime.now()}] Getting driver notifications...")
    try:
        response = requests.get(f"{BASE_URL}/drivers/{driver_id}/notifications")
        print(f"Get Notifications Status Code: {response.status_code}")
        print(f"Get Notifications Response: {response.json()}")
    except Exception as e:
        print(f"Error getting notifications: {e}")
    
    # Test listing all drivers
    print(f"\n[{datetime.now()}] Listing all drivers...")
    try:
        response = requests.get(f"{BASE_URL}/drivers/")
        print(f"List Drivers Status Code: {response.status_code}")
        print(f"List Drivers Response: {response.json()}")
    except Exception as e:
        print(f"Error listing drivers: {e}")

if __name__ == "__main__":
    test_driver_endpoints()