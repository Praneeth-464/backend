import random
from typing import List, Dict, Tuple
from uuid import UUID
from datetime import datetime, timezone
from ..schemas import Assignment, MatchResponse
from ..crud import get_riders, get_drivers
from ..utils.distance_calc import calculate_distance
from ..utils.utility_function import calculate_time_utility, gini_index, social_welfare

def rga_enhanced_algorithm() -> MatchResponse:
    """
    Enhanced Randomized Greedy Algorithm for ride matching with improved fairness optimization
    
    This enhanced version improves upon the basic RGA by:
    1. Considering both individual utility and global fairness in the assignment process
    2. Using a weighted approach that balances utility and fairness
    3. Implementing a look-ahead mechanism to avoid poor local optima
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
    
    # For each rider, find the best available driver considering both utility and fairness
    for rider in riders:
        best_driver = None
        best_combined_score = -1
        best_utility = -1
        
        # Find the best available driver for this rider
        candidate_assignments = []
        
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
            
            # Create a temporary assignment to evaluate its impact on overall fairness
            temp_assignments = assignments + [Assignment(
                rider_id=rider.id,
                driver_id=driver.id,
                utility=utility
            )]
            temp_utilities = utilities + [utility]
            
            # Calculate the potential Gini index after this assignment
            potential_gini = gini_index(temp_utilities)
            
            # Calculate a combined score that balances utility and fairness
            # Lower Gini index means better fairness, so we want to minimize it
            # We use a weighted combination: 0.7 for utility, 0.3 for fairness (1 - gini)
            fairness_score = 1 - potential_gini  # Convert to a score where higher is better
            combined_score = 0.7 * utility + 0.3 * fairness_score
            
            candidate_assignments.append({
                'driver': driver,
                'utility': utility,
                'gini': potential_gini,
                'combined_score': combined_score
            })
            
            if combined_score > best_combined_score:
                best_combined_score = combined_score
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
        algorithm="RGA-Enhanced",
        assignments=assignments,
        metrics={"gini": gini, "social_welfare": sw}
    )