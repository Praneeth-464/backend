from fastapi import APIRouter, HTTPException
from uuid import UUID
from ..schemas import FareEstimateRequest, FareEstimateResponse, AlgorithmFareEstimateRequest, AlgorithmFareEstimateResponse
from ..crud import estimate_fare
from ..utils.datetime_serializer import simple_datetime_handler
from ..algorithms.rga import rga_algorithm
from ..algorithms.rga_plus import rga_plus_algorithm
from ..algorithms.iterative_voting import iterative_voting_algorithm
from ..utils.distance_calc import calculate_distance
import traceback

router = APIRouter()

@router.post("/estimate", response_model=FareEstimateResponse)
async def estimate_ride_fare(request: FareEstimateRequest):
    """
    Estimate fare for a ride based on origin, destination, and other factors
    """
    try:
        fare_estimate = estimate_fare(
            request.origin_lat,
            request.origin_lon,
            request.destination_lat,
            request.destination_lon,
            request.rider_beta or 0.5,
            request.traffic_multiplier or 1.0
        )
        
        return simple_datetime_handler(fare_estimate)
    except Exception as e:
        print(f"Error in estimate_ride_fare: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error estimating fare: {str(e)}")

@router.post("/estimate/algorithm", response_model=AlgorithmFareEstimateResponse)
async def estimate_ride_fare_by_algorithm(request: AlgorithmFareEstimateRequest):
    """
    Estimate fare for a ride based on origin, destination, and algorithm
    """
    try:
        # Calculate distance
        distance_km = calculate_distance(
            request.origin_lat,
            request.origin_lon,
            request.destination_lat,
            request.destination_lon
        )
        
        # Base fare components
        base_fare = 2.50  # Base fare in currency units
        distance_rate = 1.25  # Per kilometer
        time_rate = 0.50  # Per minute
        
        # Estimated time (assuming average speed of 30 km/h)
        estimated_duration_minutes = (distance_km / 30) * 60 * (request.traffic_multiplier or 1.0)
        
        # Calculate fare components
        distance_fare = distance_km * distance_rate
        time_fare = estimated_duration_minutes * time_rate
        
        # Apply surge pricing during peak hours (simplified)
        from datetime import datetime, timezone
        current_hour = datetime.now(timezone.utc).hour
        surge_multiplier = 1.0
        if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:  # Peak hours
            surge_multiplier = 1.25
        
        # Apply rider's patience factor (higher beta might get slight discount)
        rider_beta = request.rider_beta or 0.5
        beta_discount = 1.0 - (rider_beta * 0.05)  # Max 5% discount for high patience
        
        estimated_fare = (base_fare + distance_fare + time_fare) * surge_multiplier * beta_discount
        
        # Run the selected algorithm to get utility and metrics
        utility = None
        metrics = None
        
        if request.algorithm == "RGA":
            result = rga_algorithm()
            # For simplicity, we'll take the average utility from assignments
            if result.assignments:
                utility = sum(a.utility for a in result.assignments) / len(result.assignments)
            metrics = result.metrics
        elif request.algorithm == "RGA++":
            result = rga_plus_algorithm()
            # For simplicity, we'll take the average utility from assignments
            if result.assignments:
                utility = sum(a.utility for a in result.assignments) / len(result.assignments)
            metrics = result.metrics
        elif request.algorithm == "IV":
            result = iterative_voting_algorithm()
            # For simplicity, we'll take the average utility from assignments
            if result.assignments:
                utility = sum(a.utility for a in result.assignments) / len(result.assignments)
            metrics = result.metrics
        
        response = AlgorithmFareEstimateResponse(
            algorithm=request.algorithm,
            estimated_fare=round(estimated_fare, 2),
            distance_km=round(distance_km, 2),
            estimated_duration_minutes=round(estimated_duration_minutes, 2),
            base_fare=base_fare,
            distance_fare=round(distance_fare, 2),
            time_fare=round(time_fare, 2),
            surge_multiplier=surge_multiplier,
            utility=utility,
            metrics=metrics
        )
        
        return simple_datetime_handler(response.dict())
    except Exception as e:
        print(f"Error in estimate_ride_fare_by_algorithm: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error estimating fare: {str(e)}")