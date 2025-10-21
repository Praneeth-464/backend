from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from uuid import UUID
import random
from datetime import datetime, timezone
from ..schemas import RiderCreate, RiderResponse, MatchResponse, DriverResponse, Assignment, RiderMatchResponse, RideCreate, RideResponse, RideRequestCreate
from ..crud import create_rider, get_rider, get_riders, update_rider, delete_rider, get_user_by_email, get_rider_by_user_id, get_driver, get_drivers, create_ride, update_ride
from ..utils.distance_calc import calculate_distance
from ..utils.utility_function import calculate_time_utility, gini_index, social_welfare
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
from ..algorithms.rga_plus import rga_plus_algorithm
import traceback

router = APIRouter()

@router.post("/", response_model=RiderResponse)
async def register_rider(rider: RiderCreate):
    """
    Register a new rider profile. Validates that the email exists in the users table.
    No JWT token required for registration.
    """
    try:
        # Check if email exists in users table
        from ..crud import get_user_by_email
        user = get_user_by_email(rider.email)
        if not user:
            raise HTTPException(status_code=400, detail="Email not found in users table. Please register as a user first.")
        
        # Check if rider already exists for this user
        from ..crud import get_rider_by_user_id
        existing_rider = get_rider_by_user_id(user.id)
        if existing_rider:
            raise HTTPException(status_code=400, detail="Rider profile already exists for this user")
        
        # Use user's ID
        user_id = user.id
        
        # Add user_id to rider data
        rider_data = rider.model_copy(update={"user_id": user_id})
        
        # Import CRUD operations
        from ..crud import create_rider, update_user_role
        
        result = create_rider(rider_data)
        
        # Update user role to 'rider'
        update_user_role(user_id, 'rider')
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(result.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in register_rider: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/request", response_model=RiderMatchResponse)
async def request_ride(rider: RideRequestCreate, background_tasks: BackgroundTasks):
    """
    Rider submits a trip request with preferences and automatically matches with available drivers.
    Validates that the email exists in the users table.
    Returns rider details along with matched driver information.
    If no drivers are available, returns an error response.
    """
    try:
        # Check if email exists in users table
        from ..crud import get_user_by_email
        user = get_user_by_email(rider.email)
        if not user:
            raise HTTPException(status_code=400, detail="Email not found in users table. Please register as a user first.")
        
        # Check if there are available drivers before proceeding
        from ..crud import get_drivers
        all_drivers = get_drivers()
        available_drivers = [d for d in all_drivers if d.available]
        
        if not available_drivers:
            raise HTTPException(status_code=400, detail="No drivers available at the moment. Please try again later.")
        
        # Get existing rider profile for this user (if any)
        from ..crud import get_rider_by_user_id
        existing_rider = get_rider_by_user_id(user.id)
        
        # Use user's ID
        user_id = user.id
        
        result = None
        if existing_rider:
            # Use existing rider profile
            result = existing_rider
            
            # Update rider profile with new request data
            updated_rider_data = RiderCreate(
                user_id=user_id,
                name=rider.name,
                email=rider.email,
                origin_lat=rider.origin_lat,
                origin_lon=rider.origin_lon,
                destination_lat=rider.destination_lat,
                destination_lon=rider.destination_lon,
                preferred_departure=rider.preferred_departure,
                preferred_arrival=rider.preferred_arrival,
                beta=rider.beta
            )
            from ..crud import update_rider
            result = update_rider(existing_rider.id, updated_rider_data)
        else:
            # Create new rider profile
            rider_data = rider.model_copy(update={"user_id": user_id})
            from ..crud import create_rider
            result = create_rider(rider_data)
            
            # Update user role to 'rider'
            from ..crud import update_user_role
            update_user_role(user_id, 'rider')
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create or update rider profile")
        
        # Create a ride record in the rides table
        from ..crud import create_ride
        ride_create = RideCreate(
            user_id=user_id,
            rider_id=result.id,
            algorithm="RGA++",
            status="requested"
        )
        ride_result = create_ride(ride_create)
        
        # Run automatic matching using RGA++ algorithm for all riders and drivers
        from ..algorithms.rga_plus import rga_plus_algorithm
        from ..crud import update_ride, get_driver
        match_result = rga_plus_algorithm()
        
        # Find if this specific rider was matched
        rider_match = None
        matched_driver = None
        matched_ride_updated = False
        
        for assignment in match_result.assignments:
            if str(assignment.rider_id) == str(result.id):
                rider_match = assignment
                # Get driver details
                matched_driver = get_driver(assignment.driver_id)
                
                # Update ride with driver assignment
                if ride_result:
                    updated_ride = RideCreate(
                        user_id=ride_result.user_id,
                        rider_id=ride_result.rider_id,
                        driver_id=assignment.driver_id,
                        algorithm="RGA++",
                        utility=assignment.utility,
                        status="assigned"
                    )
                    # Update the ride record with the matched driver
                    update_ride(ride_result.id, updated_ride)
                    matched_ride_updated = True
                break
        
        # If this rider wasn't matched but we have a ride record, update its status
        if not matched_ride_updated and ride_result:
            updated_ride = RideCreate(
                user_id=ride_result.user_id,
                rider_id=ride_result.rider_id,
                algorithm="RGA++",
                status="no_drivers_available"
            )
            update_ride(ride_result.id, updated_ride)
        
        # Prepare response with rider and driver details
        response_data = result.dict()
        if matched_driver:
            response_data['matched_driver'] = matched_driver.dict()
            response_data['match_details'] = {
                'algorithm': match_result.algorithm,
                'utility': rider_match.utility if rider_match else None,
                'metrics': match_result.metrics
            }
            # Send notification in background if matched
            if rider_match:
                from ..routes.riders import send_ride_notification
                background_tasks.add_task(send_ride_notification, result, matched_driver, rider_match)
        else:
            # No driver was matched for this specific rider, but drivers may still be available
            response_data['matched_driver'] = None
            response_data['match_details'] = None
            
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(response_data)
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in request_ride: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

def send_ride_notification(rider: RiderResponse, driver: DriverResponse, assignment: Assignment):
    """
    Send notification about ride assignment (simplified implementation)
    """
    print(f"Notification: Rider {rider.name} matched with Driver {driver.name}")
    print(f"Ride details: Pickup at ({rider.origin_lat}, {rider.origin_lon}) to ({rider.destination_lat}, {rider.destination_lon})")
    print(f"Utility score: {assignment.utility}")

@router.get("/", response_model=List[RiderResponse])
async def list_riders():
    """
    Get all riders
    """
    try:
        result = get_riders()
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([rider.dict() for rider in result])
        return serialized_result
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in list_riders: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving riders: {str(e)}")

@router.get("/me", response_model=RiderResponse)
async def get_current_rider(current_user_email: str = Depends(get_current_user)):
    """
    Get the rider profile for the currently authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get rider by user ID
        rider = get_rider_by_user_id(user.id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider profile not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(rider.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_current_rider: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving rider: {str(e)}")

@router.get("/{rider_id}", response_model=RiderResponse)
async def get_rider_by_id(rider_id: UUID):
    """
    Get a specific rider by ID
    """
    try:
        rider = get_rider(rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(rider.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_rider_by_id: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving rider: {str(e)}")

@router.put("/me", response_model=RiderResponse)
async def update_current_rider(rider: RiderCreate, current_user_email: str = Depends(get_current_user)):
    """
    Update the rider profile for the currently authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get rider by user ID
        existing_rider = get_rider_by_user_id(user.id)
        if not existing_rider:
            raise HTTPException(status_code=404, detail="Rider profile not found")
        
        # Update rider
        updated_rider = update_rider(existing_rider.id, rider)
        if not updated_rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(updated_rider.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in update_current_rider: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating rider: {str(e)}")

@router.delete("/me")
async def delete_current_rider(current_user_email: str = Depends(get_current_user)):
    """
    Delete the rider profile for the currently authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get rider by user ID
        rider = get_rider_by_user_id(user.id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider profile not found")
        
        # Delete rider
        success = delete_rider(rider.id)
        if not success:
            raise HTTPException(status_code=404, detail="Rider not found")
        return {"message": "Rider deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in delete_current_rider: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error deleting rider: {str(e)}")

@router.get("/me/rides", response_model=List[RideResponse])
async def get_current_rider_rides(current_user_email: str = Depends(get_current_user)):
    """
    Get all rides for the currently authenticated rider
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=4404, detail="User not found")
        
        # Get rider by user ID
        rider = get_rider_by_user_id(user.id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider profile not found")
        
        # Get all rides for this rider
        from ..crud import get_rides_by_rider
        rides = get_rides_by_rider(rider.id)
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([ride.dict() for ride in rides])
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_current_rider_rides: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving rides: {str(e)}")

@router.get("/{rider_id}/rides", response_model=List[RideResponse])
async def get_rider_rides(rider_id: UUID):
    """
    Get all rides for a specific rider by rider ID
    """
    try:
        # Check if rider exists
        rider = get_rider(rider_id)
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        
        # Get all rides for this rider
        from ..crud import get_rides_by_rider
        rides = get_rides_by_rider(rider_id)
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([ride.dict() for ride in rides])
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_rider_rides: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving rides: {str(e)}")
