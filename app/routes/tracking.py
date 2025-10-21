from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import Dict, Any, Optional
from ..schemas import RideResponse
from ..crud import get_ride, get_driver, get_rider, get_user_by_email, update_driver_location
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
from ..database import get_supabase_client
import traceback
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.get("/rides/{ride_id}")
async def get_ride_tracking(ride_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Get real-time tracking information for an active ride
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get ride information
        ride = get_ride(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        # Verify user has access to this ride (either as rider or driver)
        # In a real implementation, you would check if the user is authorized to view this ride
        # For now, we'll just verify the ride exists
        
        # Get driver information
        driver = get_driver(ride.driver_id) if ride.driver_id else None
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        # Get rider information
        rider = get_rider(ride.rider_id) if ride.rider_id else None
        if not rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        
        # Calculate estimated arrival time (simplified)
        # In a real implementation, this would use actual routing algorithms
        estimated_arrival = datetime.now(timezone.utc) + timedelta(minutes=5)
        eta_dropoff = estimated_arrival + timedelta(minutes=20)
        
        # Calculate distance to pickup (simplified)
        distance_to_pickup = 1.2  # km
        
        tracking_info = {
            "ride_id": str(ride_id),
            "driver_location": {
                "lat": driver.current_lat,
                "lon": driver.current_lon
            },
            "estimated_arrival": estimated_arrival,
            "distance_to_pickup": distance_to_pickup,
            "eta_dropoff": eta_dropoff
        }
        
        return simple_datetime_handler(tracking_info)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_ride_tracking: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving tracking information: {str(e)}")

@router.post("/drivers/{driver_id}/location")
async def update_driver_location_realtime(driver_id: UUID, location: Dict[str, float], current_user_email: str = Depends(get_current_user)):
    """
    Update driver location for real-time tracking
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify the driver is the authenticated user
        # In a real implementation, you would check if the user is authorized to update this driver's location
        # For now, we'll just process the request
        
        lat = location.get("lat")
        lon = location.get("lon")
        speed = location.get("speed", 0.0)
        heading = location.get("heading", 0.0)
        
        if lat is None or lon is None:
            raise HTTPException(status_code=400, detail="Latitude and longitude are required")
        
        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise HTTPException(status_code=400, detail="Invalid coordinates")
        
        # Update the driver's location in the database
        driver = update_driver_location_for_tracking(driver_id, lat, lon, speed, heading, user.id)
        
        response = {
            "message": "Location updated successfully",
            "timestamp": datetime.now(timezone.utc),
            "driver_id": str(driver_id),
            "location": {
                "lat": lat,
                "lon": lon,
                "speed": speed,
                "heading": heading
            }
        }
        
        return simple_datetime_handler(response)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_driver_location_realtime: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating driver location: {str(e)}")

# Function to update driver location with additional tracking data
def update_driver_location_for_tracking(driver_id: UUID, lat: float, lon: float, speed: float, heading: float, user_id: Optional[UUID] = None) -> Any:
    """
    Update driver location with tracking information
    In a real implementation, this would update a separate tracking table
    """
    # For now, we'll just update the driver's current location
    # In a real implementation, we would also store speed and heading in a tracking table
    # Also insert into tracking table with user_id
    from ..utils.datetime_serializer import simple_datetime_handler
    
    supabase = get_supabase_client()
    
    # Insert tracking data
    tracking_data = {
        "user_id": str(user_id) if user_id else None,
        "driver_id": str(driver_id),
        "lat": lat,
        "lon": lon,
        "speed": speed,
        "heading": heading,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        supabase.table("tracking").insert(tracking_data).execute()
    except Exception as e:
        print(f"Error inserting tracking data: {e}")
    
    return update_driver_location(driver_id, lat, lon, True)