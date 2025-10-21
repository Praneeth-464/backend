import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_scheduled_rides_functionality():
    """
    Test the scheduled rides functionality
    """
    print("Testing scheduled rides functionality...")
    
    # First, let's create a rider (you'll need a valid rider ID)
    print(f"\n[{datetime.now()}] You'll need a valid rider ID to test scheduled rides.")
    rider_id = input("Enter a valid rider ID: ")
    
    # Test scheduling a ride
    print(f"\n[{datetime.now()}] Scheduling a ride...")
    scheduled_time = (datetime.now() + timedelta(hours=2)).isoformat()
    
    schedule_request = {
        "rider_id": rider_id,
        "origin_lat": 12.9716,
        "origin_lon": 77.5946,
        "destination_lat": 13.0358,
        "destination_lon": 77.5970,
        "scheduled_time": scheduled_time,
        "preferences": {
            "min_driver_rating": 4.5,
            "ride_type": "solo"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/scheduled-rides/", json=schedule_request)
        print(f"Schedule Ride Status Code: {response.status_code}")
        schedule_response = response.json()
        print(f"Schedule Ride Response: {schedule_response}")
        
        if response.status_code == 200:
            ride_id = schedule_response["id"]
            
            # Test getting scheduled rides for the rider
            print(f"\n[{datetime.now()}] Getting scheduled rides for rider...")
            response = requests.get(f"{BASE_URL}/scheduled-rides/rider/{rider_id}")
            print(f"Get Scheduled Rides Status Code: {response.status_code}")
            print(f"Get Scheduled Rides Response: {response.json()}")
            
            # Test updating ride status
            print(f"\n[{datetime.now()}] Updating ride status to 'confirmed'...")
            response = requests.put(f"{BASE_URL}/scheduled-rides/{ride_id}/status/confirmed")
            print(f"Update Status Status Code: {response.status_code}")
            print(f"Update Status Response: {response.json()}")
    except Exception as e:
        print(f"Error testing scheduled rides: {e}")

if __name__ == "__main__":
    test_scheduled_rides_functionality()