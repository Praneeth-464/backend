from fastapi import APIRouter, HTTPException
from uuid import UUID
from datetime import datetime, timezone
from ..schemas import AnalyticsRequest, AnalyticsResponse
from ..crud import get_user_analytics, get_system_metrics, get_rides, get_rider, get_driver, get_driver_earnings
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.utility_function import gini_index, social_welfare
import traceback

router = APIRouter()

@router.post("/user", response_model=AnalyticsResponse)
async def get_user_analytics_endpoint(request: AnalyticsRequest):
    """
    Get analytics for a user
    """
    try:
        analytics = get_user_analytics(
            request.user_id,
            request.start_date,
            request.end_date
        )
        
        return simple_datetime_handler(analytics)
    except Exception as e:
        print(f"Error in get_user_analytics_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user analytics: {str(e)}")

@router.get("/user/{user_id}")
async def get_user_analytics_simple(user_id: UUID):
    """
    Get analytics for a user (simple endpoint)
    """
    try:
        analytics = get_user_analytics(user_id)
        return simple_datetime_handler(analytics)
    except Exception as e:
        print(f"Error in get_user_analytics_simple: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user analytics: {str(e)}")

@router.get("/system")
async def get_system_metrics_endpoint():
    """
    Retrieve overall system performance metrics
    """
    try:
        # Get real system metrics from the database
        metrics = get_system_metrics()
        metrics["timestamp"] = datetime.now(timezone.utc)
        
        return simple_datetime_handler(metrics)
    except Exception as e:
        print(f"Error in get_system_metrics_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving system metrics: {str(e)}")

@router.get("/algorithms")
async def get_algorithm_performance():
    """
    Retrieve performance metrics for matching algorithms
    """
    try:
        # In a real implementation, this would query the database for historical algorithm performance
        # For now, we'll return real data based on existing rides
        
        # Get all rides to analyze algorithm usage
        rides = get_rides()
        
        # Group rides by algorithm
        algorithm_stats = {}
        for ride in rides:
            algorithm = ride.algorithm or "Unknown"
            if algorithm not in algorithm_stats:
                algorithm_stats[algorithm] = {
                    "count": 0,
                    "utilities": [],
                    "total_time": 0
                }
            algorithm_stats[algorithm]["count"] += 1
            if ride.utility:
                algorithm_stats[algorithm]["utilities"].append(ride.utility)
        
        # Calculate metrics for each algorithm
        algorithms = []
        for algorithm, stats in algorithm_stats.items():
            gini = gini_index(stats["utilities"]) if stats["utilities"] else 0.0
            sw = social_welfare(stats["utilities"]) if stats["utilities"] else 0.0
            
            algorithms.append({
                "name": algorithm,
                "gini_index": round(gini, 4),
                "social_welfare": round(sw, 4),
                "execution_time": round(stats["total_time"] / stats["count"] if stats["count"] > 0 else 0, 4),
                "usage_count": stats["count"]
            })
        
        response = {
            "algorithms": algorithms,
            "timestamp": datetime.now(timezone.utc)
        }
        
        return simple_datetime_handler(response)
    except Exception as e:
        print(f"Error in get_algorithm_performance: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving algorithm performance: {str(e)}")

@router.get("/users/{user_id}")
async def get_user_analytics(user_id: UUID):
    """
    Retrieve analytics for a specific user
    """
    try:
        # Get all rides for this user
        # Note: We would need to modify the rides table to include user_id or join with riders table
        # For now, we'll simulate this with rider_id
        
        # Get rider information
        rider = get_rider(user_id) if get_rider(user_id) else None  # This is a simplification
        
        # Get all rides (in a real implementation, we would filter by user)
        rides = get_rides()
        
        # Calculate user analytics
        total_rides = len(rides)
        total_spent = sum(ride.fare or 0 for ride in rides)
        
        # Favorite destinations (simplified)
        destinations = {}
        for ride in rides:
            # In a real implementation, we would get actual destination names
            dest_key = f"{ride.rider_id}"  # Simplified
            destinations[dest_key] = destinations.get(dest_key, 0) + 1
        
        favorite_destinations = [
            {"location": dest, "count": count} 
            for dest, count in sorted(destinations.items(), key=lambda x: x[1], reverse=True)[:3]
        ]
        
        analytics = {
            "user_id": str(user_id),
            "total_rides": total_rides,
            "total_spent": round(total_spent, 2),
            "favorite_destinations": favorite_destinations,
            "preferred_time": "Evening",  # Simplified
            "timestamp": datetime.now(timezone.utc)
        }
        
        return simple_datetime_handler(analytics)
    except Exception as e:
        print(f"Error in get_user_analytics: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user analytics: {str(e)}")

@router.get("/drivers/{driver_id}/earnings")
async def get_driver_earnings_endpoint(driver_id: UUID):
    """
    Retrieve a driver's earnings and statistics
    """
    try:
        # Verify the driver exists
        driver = get_driver(driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        # Get real driver earnings from the database
        earnings = get_driver_earnings(driver_id)
        
        return simple_datetime_handler(earnings.dict())
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_driver_earnings_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver earnings: {str(e)}")