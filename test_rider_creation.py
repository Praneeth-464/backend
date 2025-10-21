#!/usr/bin/env python3
"""
Test script to verify rider creation with datetime handling
"""

from datetime import datetime
from app.schemas import RiderCreate

def test_rider_creation():
    """Test rider creation with datetime fields"""
    
    # Create a rider with datetime fields
    rider = RiderCreate(
        name="John Doe",
        email="john.doe@example.com",
        origin_lat=12.9716,
        origin_lon=77.5946,
        destination_lat=13.0358,
        destination_lon=77.5970,
        preferred_departure=datetime.now(),
        preferred_arrival=datetime.now(),
        beta=0.7
    )
    
    print(f"Original rider object: {rider}")
    
    # Test model_dump with mode="json"
    json_data = rider.model_dump(mode="json")
    print(f"JSON serialized data: {json_data}")
    
    # Verify it's JSON serializable
    import json
    try:
        json_string = json.dumps(json_data)
        print(f"JSON serialization successful: {json_string}")
        print("SUCCESS: Rider data is properly JSON serializable")
    except Exception as e:
        print(f"JSON serialization failed: {e}")
        print("FAILURE: Rider data is not properly JSON serializable")

if __name__ == "__main__":
    test_rider_creation()