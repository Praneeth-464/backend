import random
from typing import List
from uuid import UUID
from datetime import datetime, timezone
from ..schemas import Assignment, MatchResponse
from ..crud import get_riders, get_drivers
from ..utils.distance_calc import calculate_distance
from ..utils.utility_function import calculate_utility, calculate_time_utility, gini_index, social_welfare

def rga_plus_algorithm() -> MatchResponse:
    """
    RGA++ Algorithm: Enhanced fairness with two-phase allocation
    Phase 1: Allocate departures (random order)
    Phase 2: Allocate arrivals (reverse order)
    """
    # Get all riders and drivers
    riders = get_riders()
    drivers = get_drivers()
    
    # Filter available drivers
    available_drivers = [d for d in drivers if d.available]
    
    assignments = []
    assigned_driver_ids = set()
    utilities = []
    
    # Phase 1: Randomly shuffle and allocate departures
    random.shuffle(riders)
    
    # First phase assignment
    for rider in riders:
        best_driver = None
        best_utility = -1
        
        # Find the best available driver for departure
        for driver in available_drivers:
            # Skip if driver already assigned
            if driver.id in assigned_driver_ids:
                continue
                
            # Calculate utility based on pickup distance
            distance = calculate_distance(
                rider.origin_lat, rider.origin_lon,
                driver.current_lat, driver.current_lon
            )
            
            # Enhanced utility function using rider preferences
            # Base utility on distance (minimum value of 0.01 to ensure positive utility)
            distance_utility = max(0.01, 1 / (1 + distance))
            
            # If rider has preferred departure time, factor it in
            time_utility = 1.0
            if rider.preferred_departure:
                # Calculate time-based utility with timezone-aware datetime
                current_time = datetime.now(timezone.utc)
                time_utility = calculate_time_utility(rider.beta or 0.5, rider.preferred_departure, current_time)
                # Ensure time utility is at least 0.01
                time_utility = max(0.01, time_utility)
            
            # Combined utility (minimum value of 0.01 to ensure positive utility)
            utility = max(0.01, distance_utility * time_utility)
            
            if utility > best_utility:
                best_utility = utility
                best_driver = driver
        
        # Assign rider to driver if found
        # Changed condition to allow assignment even with low utility
        if best_driver:
            assignment = Assignment(
                rider_id=rider.id,
                driver_id=best_driver.id,
                utility=best_utility
            )
            assignments.append(assignment)
            assigned_driver_ids.add(best_driver.id)
            utilities.append(best_utility)
    
    # Phase 2: Reverse order allocation for arrivals (simplified implementation)
    # In a full implementation, this would optimize for arrival times as well
    
    # Calculate metrics
    gini = gini_index(utilities)
    sw = social_welfare(utilities)
    
    return MatchResponse(
        algorithm="RGA++",
        assignments=assignments,
        metrics={"gini": gini, "social_welfare": sw}
    )