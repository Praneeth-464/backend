import math
from typing import List
from datetime import datetime, timezone

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def calculate_utility(beta: float, scheduled_time: float, preferred_time: float) -> float:
    """
    Calculate utility based on patience factor and time difference
    """
    time_diff = abs(scheduled_time - preferred_time)
    return 1 - (1 - beta) * time_diff

def calculate_time_utility(beta: float, preferred_time: datetime, current_time: datetime) -> float:
    """
    Calculate time-based utility using datetime objects
    """
    if preferred_time is None:
        return 1.0
    
    # Ensure both datetime objects are timezone-aware
    if isinstance(preferred_time, str):
        # Parse string datetime
        try:
            preferred_time = datetime.fromisoformat(preferred_time)
        except ValueError:
            # If parsing fails, return default utility
            return 1.0
    
    if preferred_time.tzinfo is None:
        # If preferred_time is naive, assume it's in UTC
        preferred_time = preferred_time.replace(tzinfo=timezone.utc)
    
    if isinstance(current_time, str):
        # Parse string datetime
        try:
            current_time = datetime.fromisoformat(current_time)
        except ValueError:
            # If parsing fails, use current time
            current_time = datetime.now(timezone.utc)
    
    if current_time.tzinfo is None:
        # If current_time is naive, make it timezone-aware
        current_time = current_time.replace(tzinfo=timezone.utc)
    
    # Calculate time difference in hours
    time_diff = abs((preferred_time - current_time).total_seconds() / 3600)
    return 1 - (1 - beta) * time_diff

def gini_index(utilities: List[float]) -> float:
    """
    Calculate Gini index for fairness measurement
    """
    if not utilities:
        return 0.0
    
    n = len(utilities)
    if n == 0:
        return 0.0
        
    mean_u = sum(utilities) / n
    if mean_u == 0:
        return 0.0
        
    num = sum(abs(ui - uj) for ui in utilities for uj in utilities)
    return num / (2 * n**2 * mean_u)

def social_welfare(utilities: List[float]) -> float:
    """
    Calculate social welfare (average utility)
    """
    if not utilities:
        return 0.0
    return sum(utilities) / len(utilities)