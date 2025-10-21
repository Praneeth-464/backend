import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_schedules_functionality():
    """
    Test the schedule management functionality
    """
    print("Testing schedule management functionality...")
    
    # 1. Run a scheduling algorithm
    print(f"\n[{datetime.now()}] Running RGA++ algorithm...")
    match_request = {
        "algorithm": "RGA++"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/schedules/run", json=match_request)
        print(f"Schedule Run Status Code: {response.status_code}")
        print(f"Schedule Run Response: {response.json()}")
        
        if response.status_code != 200:
            print("Schedule run failed. Exiting test.")
            return
            
        schedule_data = response.json()
        schedule_id = schedule_data.get("schedule_id")
        
    except Exception as e:
        print(f"Error running schedule: {e}")
        return
    
    # 2. List all schedules
    print(f"\n[{datetime.now()}] Listing all schedules...")
    try:
        response = requests.get(f"{BASE_URL}/schedules/")
        print(f"List Schedules Status Code: {response.status_code}")
        print(f"List Schedules Response: {response.json()}")
    except Exception as e:
        print(f"Error listing schedules: {e}")
    
    # 3. Get the specific schedule
    if schedule_id:
        print(f"\n[{datetime.now()}] Getting schedule by ID: {schedule_id}")
        try:
            response = requests.get(f"{BASE_URL}/schedules/{schedule_id}")
            print(f"Get Schedule Status Code: {response.status_code}")
            print(f"Get Schedule Response: {response.json()}")
        except Exception as e:
            print(f"Error getting schedule: {e}")
    
    # 4. Delete the schedule
    if schedule_id:
        print(f"\n[{datetime.now()}] Deleting schedule: {schedule_id}")
        try:
            response = requests.delete(f"{BASE_URL}/schedules/{schedule_id}")
            print(f"Delete Schedule Status Code: {response.status_code}")
            print(f"Delete Schedule Response: {response.json()}")
        except Exception as e:
            print(f"Error deleting schedule: {e}")

if __name__ == "__main__":
    test_schedules_functionality()