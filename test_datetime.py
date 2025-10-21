#!/usr/bin/env python3
"""
Test script to verify datetime handling with database format
"""

from datetime import datetime
from app.utils.datetime_serializer import simple_datetime_handler, format_datetime_for_db, parse_datetime_from_db

def test_datetime_handling():
    """Test datetime handling functions"""
    
    # Test with a datetime object
    now = datetime.now()
    print(f"Original datetime: {now}")
    
    # Test simple datetime handler
    result = simple_datetime_handler(now)
    print(f"Simple handler result: {result}")
    
    # Test format for database
    db_format = format_datetime_for_db(now)
    print(f"Database format: {db_format}")
    
    # Test parse from database
    parsed = parse_datetime_from_db(db_format)
    print(f"Parsed from DB: {parsed}")
    
    # Test with dictionary containing datetime
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "preferred_departure": now,
        "preferred_arrival": "2025-10-16T09:00:00+05:30",
        "beta": 0.7
    }
    
    print(f"\nOriginal data: {test_data}")
    
    # Test simple datetime handler on dictionary
    serialized_data = simple_datetime_handler(test_data)
    print(f"Serialized data: {serialized_data}")
    
    # Verify it's JSON serializable
    import json
    try:
        json_string = json.dumps(serialized_data)
        print(f"JSON serialization successful: {json_string}")
    except Exception as e:
        print(f"JSON serialization failed: {e}")

if __name__ == "__main__":
    test_datetime_handling()