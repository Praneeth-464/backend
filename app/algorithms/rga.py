import random
from typing import List, Dict
from uuid import UUID
from datetime import datetime, timezone
from ..schemas import Assignment, MatchResponse
from ..crud import get_riders, get_drivers
from ..utils.distance_calc import calculate_distance
from ..utils.utility_function import calculate_utility, calculate_time_utility, gini_index, social_welfare

def rga_algorithm() -> MatchResponse:
    """
    Randomized Greedy Algorithm for ride matching
    """
    # Get all riders and drivers
    riders = get_riders()
    drivers = get_drivers()
    
    # Filter available drivers
    available_drivers = [d for d in drivers if d.available]
    
    # Randomly shuffle riders
    random.shuffle(riders)
    
    assignments = []
    assigned_driver_ids = set()
    utilities = []
    
    # For each rider, find the best available driver
    for rider in riders:
        best_driver = None
        best_utility = -1
        
        # Find the best available driver for this rider
        for driver in available_drivers:
            # Skip if driver already assigned
            if driver.id in assigned_driver_ids:
                continue
                
            # Calculate utility based on distance and rider preferences
            distance = calculate_distance(
                rider.origin_lat, rider.origin_lon,
                driver.current_lat, driver.current_lon
            )
            
            # Enhanced utility function using rider preferences
            # Base utility on distance
            distance_utility = 1 / (1 + distance)
            
            # If rider has preferred departure time, factor it in
            time_utility = 1.0
            if rider.preferred_departure:
                # Calculate time-based utility with timezone-aware datetime
                current_time = datetime.now(timezone.utc)
                time_utility = calculate_time_utility(rider.beta or 0.5, rider.preferred_departure, current_time)
            
            # Combined utility
            utility = distance_utility * time_utility
            
            if utility > best_utility:
                best_utility = utility
                best_driver = driver
        
        # Assign rider to driver if found
        if best_driver and best_utility > 0:
            assignment = Assignment(
                rider_id=rider.id,
                driver_id=best_driver.id,
                utility=best_utility
            )
            assignments.append(assignment)
            assigned_driver_ids.add(best_driver.id)
            utilities.append(best_utility)
    
    # Calculate metrics
    gini = gini_index(utilities)
    sw = social_welfare(utilities)
    
    return MatchResponse(
        algorithm="RGA",
        assignments=assignments,
        metrics={"gini": gini, "social_welfare": sw}
    )