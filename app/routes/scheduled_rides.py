from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List
from ..schemas import ScheduledRideRequest, ScheduledRideResponse
from ..crud import create_scheduled_ride, get_scheduled_rides_by_rider, update_scheduled_ride_status, get_user_by_email, get_rider_by_user_id
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.post("/", response_model=ScheduledRideResponse)
async def schedule_ride(request: ScheduledRideRequest, current_user_email: str = Depends(get_current_user)):
    """
    Schedule a ride for a future time
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use current user's ID if not provided in request
        user_id = request.user_id if request.user_id else user.id
        
        # If rider_id is not provided, try to get rider associated with current user
        rider_id = request.rider_id
        if not rider_id:
            rider = get_rider_by_user_id(user.id)
            if not rider:
                raise HTTPException(status_code=400, detail="Rider profile not found for current user")
            rider_id = rider.id
        
        scheduled_ride = create_scheduled_ride(
            rider_id,
            request.origin_lat,
            request.origin_lon,
            request.destination_lat,
            request.destination_lon,
            request.scheduled_time,
            request.preferences.dict() if request.preferences else None,
            user_id
        )
        
        if not scheduled_ride:
            raise HTTPException(status_code=500, detail="Error scheduling ride")
        
        return simple_datetime_handler(scheduled_ride)
    except Exception as e:
        print(f"Error in schedule_ride: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error scheduling ride: {str(e)}")

@router.get("/rider", response_model=List[ScheduledRideResponse])
async def get_scheduled_rides(current_user_email: str = Depends(get_current_user)):
    """
    Get all scheduled rides for the authenticated user
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
        
        scheduled_rides = get_scheduled_rides_by_rider(rider.id)
        return simple_datetime_handler(scheduled_rides)
    except Exception as e:
        print(f"Error in get_scheduled_rides: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving scheduled rides: {str(e)}")

@router.put("/{ride_id}/status/{status}")
async def update_scheduled_ride_status_endpoint(ride_id: UUID, status: str, current_user_email: str = Depends(get_current_user)):
    """
    Update the status of a scheduled ride
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate status
        valid_statuses = ["scheduled", "confirmed", "completed", "cancelled"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        # In a real implementation, you would verify the user owns this scheduled ride
        updated_ride = update_scheduled_ride_status(ride_id, status)
        if not updated_ride:
            raise HTTPException(status_code=404, detail="Scheduled ride not found")
        
        return simple_datetime_handler(updated_ride)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_scheduled_ride_status_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating scheduled ride status: {str(e)}")