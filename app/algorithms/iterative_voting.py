from typing import List, Dict
from uuid import UUID
from datetime import datetime, timezone
from ..schemas import Assignment, MatchResponse
from ..crud import get_riders, get_drivers
from ..utils.distance_calc import calculate_distance
from ..utils.utility_function import calculate_utility, calculate_time_utility, gini_index, social_welfare

def iterative_voting_algorithm(voting_rule: str = "borda") -> MatchResponse:
    """
    Iterative Voting Algorithm for ride matching
    Riders vote among candidate routes using selected voting rule
    """
    # Get all riders and drivers
    riders = get_riders()
    drivers = get_drivers()
    
    # Filter available drivers
    available_drivers = [d for d in drivers if d.available]
    
    assignments = []
    assigned_driver_ids = set()
    utilities = []
    
    # For each rider, create a preference list of drivers
    rider_preferences = {}
    
    for rider in riders:
        driver_scores = []
        
        # Score each available driver
        for driver in available_drivers:
            if driver.id in assigned_driver_ids:
                continue
                
            # Calculate score based on distance
            distance = calculate_distance(
                rider.origin_lat, rider.origin_lon,
                driver.current_lat, driver.current_lon
            )
            
            # Enhanced scoring using rider preferences
            # Base score on distance (lower distance = higher score)
            distance_score = 1 / (1 + distance)
            
            # If rider has preferred departure time, factor it in
            time_score = 1.0
            if rider.preferred_departure:
                # Calculate time-based utility with timezone-aware datetime
                current_time = datetime.now(timezone.utc)
                time_score = calculate_time_utility(rider.beta or 0.5, rider.preferred_departure, current_time)
            
            # Combined score
            score = distance_score * time_score
            driver_scores.append((driver.id, score))
        
        # Sort by score (descending)
        driver_scores.sort(key=lambda x: x[1], reverse=True)
        rider_preferences[rider.id] = [driver_id for driver_id, _ in driver_scores]
    
    # Apply voting rule (simplified implementation)
    # In a full implementation, this would use more sophisticated voting mechanisms
    
    # Simple assignment based on preferences
    for rider in riders:
        if rider.id not in rider_preferences:
            continue
            
        # Find the highest-ranked available driver
        for driver_id in rider_preferences[rider.id]:
            if driver_id not in assigned_driver_ids:
                # Calculate utility
                rider_obj = next((r for r in riders if r.id == rider.id), None)
                driver_obj = next((d for d in available_drivers if d.id == driver_id), None)
                
                if rider_obj and driver_obj:
                    distance = calculate_distance(
                        rider_obj.origin_lat, rider_obj.origin_lon,
                        driver_obj.current_lat, driver_obj.current_lon
                    )
                    
                    # Enhanced utility calculation using preferences
                    distance_utility = 1 / (1 + distance)
                    time_utility = 1.0
                    if rider_obj.preferred_departure:
                        current_time = datetime.now(timezone.utc)
                        time_utility = calculate_time_utility(rider_obj.beta or 0.5, rider_obj.preferred_departure, current_time)
                    utility = distance_utility * time_utility
                    
                    assignment = Assignment(
                        rider_id=rider.id,
                        driver_id=driver_id,
                        utility=utility
                    )
                    assignments.append(assignment)
                    assigned_driver_ids.add(driver_id)
                    utilities.append(utility)
                break
    
    # Calculate metrics
    gini = gini_index(utilities)
    sw = social_welfare(utilities)
    
    return MatchResponse(
        algorithm="IV",
        assignments=assignments,
        metrics={"gini": gini, "social_welfare": sw}
    )

def borda_voting(riders: List, available_drivers: List) -> MatchResponse:
    """
    Borda Count Voting Rule
    """
    return iterative_voting_algorithm("borda")

def instant_runoff_voting(riders: List, available_drivers: List) -> MatchResponse:
    """
    Instant Runoff Voting Rule
    """
    return iterative_voting_algorithm("instant_runoff")

def harmonic_voting(riders: List, available_drivers: List) -> MatchResponse:
    """
    Harmonic Mean Voting Rule
    """
    return iterative_voting_algorithm("harmonic")

def popularity_voting(riders: List, available_drivers: List) -> MatchResponse:
    """
    Popularity Voting Rule
    """
    return iterative_voting_algorithm("popularity")