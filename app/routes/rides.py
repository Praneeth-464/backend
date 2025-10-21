from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from ..schemas import RideCreate, RideResponse, EstimatedFareResponse
from ..crud import get_rides, get_ride, create_ride, update_ride, get_rider, get_user_by_email, get_rider_by_user_id, get_rides_by_user_id
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.get("/", response_model=List[RideResponse])
async def list_rides(current_user_email: str = Depends(get_current_user)):
    """
    Retrieve all ride records for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get rides for the current user
        result = get_rides_by_user_id(user.id)
        serialized_result = simple_datetime_handler([ride.dict() for ride in result])
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in list_rides: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving rides: {str(e)}")

@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride_by_id(ride_id: UUID):
    """
    Retrieve a specific ride by ID
    """
    try:
        ride = get_ride(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        # Convert to dict and handle datetime serialization
        ride_dict = ride.dict()
        
        # If fare is null, calculate estimated fare
        if ride_dict.get("fare") is None:
            try:
                # Get rider information to get origin and destination coordinates
                rider = get_rider(ride.rider_id) if ride.rider_id else None
                if rider:
                    # Import the fare estimation function
                    from ..crud import estimate_fare
                    
                    # Estimate fare based on rider's origin and destination
                    fare_estimate = estimate_fare(
                        rider.origin_lat,
                        rider.origin_lon,
                        rider.destination_lat,
                        rider.destination_lon,
                        rider.beta or 0.5,  # Use rider's beta value or default to 0.5
                        1.0  # Default traffic multiplier
                    )
                    
                    # Set the estimated fare in the response
                    ride_dict["fare"] = fare_estimate["estimated_fare"]
            except Exception as e:
                # If fare estimation fails, continue with null fare
                print(f"Error estimating fare for ride {ride_id}: {str(e)}")
        
        serialized_result = simple_datetime_handler(ride_dict)
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_ride_by_id: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving ride: {str(e)}")

@router.post("/", response_model=RideResponse)
async def create_new_ride(ride: RideCreate, current_user_email: str = Depends(get_current_user)):
    """
    Create a new ride record for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use current user's ID if not provided in request
        user_id = ride.user_id if ride.user_id else user.id
        
        # Get rider profile for the current user
        rider = get_rider_by_user_id(user.id)
        if not rider:
            raise HTTPException(status_code=400, detail="Rider profile not found for current user. Please create a rider profile first.")
        
        # Use rider ID from user's rider profile
        rider_id = ride.rider_id if ride.rider_id else rider.id
        
        # Add user_id and rider_id to ride data
        ride_data = ride.model_copy(update={"user_id": user_id, "rider_id": rider_id})
        
        result = create_ride(ride_data)
        serialized_result = simple_datetime_handler(result.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_new_ride: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{ride_id}", response_model=RideResponse)
async def update_ride_record(ride_id: UUID, ride: RideCreate):
    """
    Update a ride record
    """
    try:
        result = update_ride(ride_id, ride)
        if not result:
            raise HTTPException(status_code=404, detail="Ride not found")
        serialized_result = simple_datetime_handler(result.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_ride_record: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating ride: {str(e)}")

@router.get("/{ride_id}/status")
async def get_ride_status(ride_id: UUID):
    """
    Get the status of a specific ride
    """
    try:
        ride = get_ride(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        # Return detailed ride status information
        status_info = {
            "id": str(ride.id),
            "rider_id": str(ride.rider_id),
            "driver_id": str(ride.driver_id) if ride.driver_id else None,
            "algorithm": ride.algorithm,
            "start_time": ride.start_time.isoformat() if ride.start_time else None,
            "end_time": ride.end_time.isoformat() if ride.end_time else None,
            "fare": ride.fare,
            "utility": ride.utility,
            "status": ride.status
        }
        
        # If fare is null, calculate estimated fare
        if status_info.get("fare") is None:
            try:
                # Get rider information to get origin and destination coordinates
                rider = get_rider(ride.rider_id) if ride.rider_id else None
                if rider:
                    # Import the fare estimation function
                    from ..crud import estimate_fare
                    
                    # Estimate fare based on rider's origin and destination
                    fare_estimate = estimate_fare(
                        rider.origin_lat,
                        rider.origin_lon,
                        rider.destination_lat,
                        rider.destination_lon,
                        rider.beta or 0.5,  # Use rider's beta value or default to 0.5
                        1.0  # Default traffic multiplier
                    )
                    
                    # Set the estimated fare in the response
                    status_info["estimated_fare"] = fare_estimate["estimated_fare"]
                    status_info["fare"] = fare_estimate["estimated_fare"]
            except Exception as e:
                # If fare estimation fails, continue with null fare
                print(f"Error estimating fare for ride {ride_id}: {str(e)}")
        
        # Add location information if available
        rider = get_rider(ride.rider_id) if ride.rider_id else None
        if rider:
            status_info["pickup_location"] = {
                "lat": rider.origin_lat,
                "lon": rider.origin_lon
            }
            status_info["dropoff_location"] = {
                "lat": rider.destination_lat,
                "lon": rider.destination_lon
            }
        
        return simple_datetime_handler(status_info)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_ride_status: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving ride status: {str(e)}")

@router.get("/{ride_id}/estimated-fare", response_model=EstimatedFareResponse)
async def get_ride_estimated_fare(ride_id: UUID):
    """
    Get the estimated fare for a specific ride
    """
    try:
        # Get the ride
        ride = get_ride(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        # Get rider information to get origin and destination coordinates
        rider = get_rider(ride.rider_id) if ride.rider_id else None
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        
        # Import the fare estimation function
        from ..crud import estimate_fare
        
        # Estimate fare based on rider's origin and destination
        fare_estimate = estimate_fare(
            rider.origin_lat,
            rider.origin_lon,
            rider.destination_lat,
            rider.destination_lon,
            rider.beta or 0.5,  # Use rider's beta value or default to 0.5
            1.0  # Default traffic multiplier
        )
        
        # Create the response object
        response_data = {
            "ride_id": ride.id,
            "algorithm": ride.algorithm,
            "status": ride.status,
            "estimated_fare": fare_estimate["estimated_fare"],
            "distance_km": fare_estimate["distance_km"],
            "estimated_duration_minutes": fare_estimate["estimated_duration_minutes"],
            "base_fare": fare_estimate["base_fare"],
            "distance_fare": fare_estimate["distance_fare"],
            "time_fare": fare_estimate["time_fare"],
            "surge_multiplier": fare_estimate["surge_multiplier"]
        }
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(response_data)
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_ride_estimated_fare: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving ride estimated fare: {str(e)}")
