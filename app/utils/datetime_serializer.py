from datetime import datetime
from typing import Any, Dict
import json

def simple_datetime_handler(obj: Any) -> Any:
    """
    Simple datetime handler that converts datetime objects to ISO format strings
    This is a simplified version for direct database compatibility
    """
    if isinstance(obj, datetime):
        # Convert datetime to ISO format string for JSON serialization
        return obj.isoformat()
    elif hasattr(obj, 'isoformat'):
        # Handle datetime-like objects that have isoformat method
        return obj.isoformat()
    elif isinstance(obj, dict):
        # Recursively handle dictionaries
        return {key: simple_datetime_handler(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        # Recursively handle lists
        return [simple_datetime_handler(item) for item in obj]
    else:
        # Return the object as is for non-datetime objects
        return obj

def format_datetime_for_db(dt_obj: Any) -> str:
    """
    Format datetime object for database insertion
    Compatible with PostgreSQL TIMESTAMPTZ format
    """
    if isinstance(dt_obj, datetime):
        return dt_obj.isoformat()
    elif isinstance(dt_obj, str):
        # Assume string is already in correct format
        return dt_obj
    else:
        # Convert to string as fallback
        return str(dt_obj)

def parse_datetime_from_db(dt_str: str) -> str:
    """
    Parse datetime string from database and ensure it's in ISO format
    This ensures compatibility with JSON serialization
    """
    if isinstance(dt_str, str):
        # Already a string, ensure it's in ISO format
        return dt_str
    elif hasattr(dt_str, 'isoformat'):
        # Convert datetime-like objects to ISO string
        return dt_str.isoformat()
    else:
        # Convert to string as fallback
        return str(dt_str)