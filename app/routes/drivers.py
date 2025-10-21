from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from ..schemas import DriverCreate, DriverResponse, DriverUpdateLocation, RideResponse, NotificationResponse, DriverEarnings
from ..crud import (
    create_driver, get_driver, get_drivers, update_driver, delete_driver, update_driver_location,
    get_rides_by_driver, get_rides,
    get_user_notifications, mark_notification_as_read,
    get_driver_earnings, get_driver_ratings, get_driver_average_rating,
    get_driver_by_user_id
)
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.post("/", response_model=DriverResponse)
async def register_driver(driver: DriverCreate):
    """
    Register a new driver profile. Validates that the email exists in the users table.
    No JWT token required for registration.
    """
    try:
        # Check if email exists in users table
        from ..crud import get_user_by_email
        user = get_user_by_email(driver.email)
        if not user:
            raise HTTPException(status_code=400, detail="Email not found in users table. Please register as a user first.")
        
        # Check if driver already exists for this user
        from ..crud import get_driver_by_user_id
        existing_driver = get_driver_by_user_id(user.id)
        if existing_driver:
            raise HTTPException(status_code=400, detail="Driver profile already exists for this user")
        
        # Use user's ID
        user_id = user.id
        
        # Add user_id to driver data
        driver_data = driver.model_copy(update={"user_id": user_id})
        
        # Import CRUD operations
        from ..crud import create_driver, update_user_role
        
        result = create_driver(driver_data)
        
        # Update user role to 'driver'
        update_user_role(user_id, 'driver')
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(result.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in register_driver: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_drivers():
    """
    Get all drivers
    """
    try:
        result = get_drivers()
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([driver.dict() for driver in result])
        return serialized_result
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in list_drivers: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving drivers: {str(e)}")

@router.get("/me")
async def get_current_driver(current_user_email: str = Depends(get_current_user)):
    """
    Get the driver profile for the currently authenticated user
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=4404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(driver.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_current_driver: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver: {str(e)}")

@router.put("/me")
async def update_current_driver(driver: DriverCreate, current_user_email: str = Depends(get_current_user)):
    """
    Update the driver profile for the currently authenticated user
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        existing_driver = get_driver_by_user_id(user.id)
        if not existing_driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
        
        # Update driver
        updated_driver = update_driver(existing_driver.id, driver)
        if not updated_driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(updated_driver.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in update_current_driver: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating driver: {str(e)}")

@router.delete("/me")
async def delete_current_driver(current_user_email: str = Depends(get_current_user)):
    """
    Delete the driver profile for the currently authenticated user
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
        
        # Delete driver
        success = delete_driver(driver.id)
        if not success:
            raise HTTPException(status_code=404, detail="Driver not found")
        return {"message": "Driver deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in delete_current_driver: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error deleting driver: {str(e)}")

@router.get("/me/rides")
async def get_current_driver_ride_history(current_user_email: str = Depends(get_current_user)):
    """
    Get ride history for the currently authenticated user
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        rides = get_rides_by_driver(driver.id)
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([ride.dict() for ride in rides])
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_current_driver_ride_history: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving ride history: {str(e)}")

@router.get("/me/earnings")
async def get_current_driver_earnings_info(current_user_email: str = Depends(get_current_user)):
    """
    Get earnings information for the currently authenticated user
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        earnings = get_driver_earnings(driver.id)
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(earnings.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_current_driver_earnings_info: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving earnings: {str(e)}")

@router.get("/me/ratings")
async def get_current_driver_ratings_info(current_user_email: str = Depends(get_current_user)):
    """
    Get ratings for the currently authenticated user
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        # Get all ratings for this driver
        ratings = get_driver_ratings(driver.id)
        
        # Get average rating
        average_rating = get_driver_average_rating(driver.id)
        
        response = {
            "driver_id": str(driver.id),
            "average_rating": average_rating,
            "total_ratings": len(ratings),
            "reviews": [rating.dict() for rating in ratings]
        }
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(response)
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_current_driver_ratings_info: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving ratings: {str(e)}")

@router.get("/me/notifications")
async def get_current_driver_notifications(current_user_email: str = Depends(get_current_user)):
    """
    Get notifications for the currently authenticated driver
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        notifications = get_user_notifications(driver.id)
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([notification.dict() for notification in notifications])
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_current_driver_notifications: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving notifications: {str(e)}")

@router.get("/{driver_id}")
async def get_driver_by_id(driver_id: UUID):
    """
    Get a specific driver by ID
    """
    try:
        driver = get_driver(driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(driver.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_driver_by_id: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver: {str(e)}")

@router.post("/me/notifications/{notification_id}/read")
async def mark_current_driver_notification_read(notification_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Mark a notification as read for the currently authenticated driver
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        notification = mark_notification_as_read(notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(notification.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in mark_current_driver_notification_read: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error marking notification as read: {str(e)}")

@router.post("/me/rides/{ride_id}/accept")
async def accept_ride(ride_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Accept a ride assignment as the currently authenticated driver
    """
    try:
        print(f"Attempting to accept ride with ID: {ride_id}")
        # Get the current user
        from ..crud import get_user_by_email, get_ride, update_ride_status
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        print(f"User found: {user.email}")
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        print(f"Driver found: {driver.name} with ID: {driver.id}")
        # Get the ride
        ride = get_ride(ride_id)
        if not ride:
            print(f"Ride with ID {ride_id} not found in database")
            raise HTTPException(status_code=404, detail="Ride not found")
            
        print(f"Ride found: {ride.id} with driver ID: {ride.driver_id} and status: {ride.status}")
        # Verify that this ride is assigned to the current driver
        if str(ride.driver_id) != str(driver.id):
            raise HTTPException(status_code=403, detail="This ride is not assigned to you")
            
        # Verify that the ride is in 'assigned' status
        if ride.status != "assigned":
            raise HTTPException(status_code=400, detail=f"Ride is in {ride.status} status and cannot be accepted")
            
        # Update ride status to 'accepted'
        updated_ride = update_ride_status(ride_id, "accepted")
        if not updated_ride:
            raise HTTPException(status_code=500, detail="Error updating ride status")
            
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(updated_ride.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in accept_ride: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error accepting ride: {str(e)}")

@router.post("/me/rides/{ride_id}/reject")
async def reject_ride(ride_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Reject a ride assignment as the currently authenticated driver
    """
    try:
        print(f"Attempting to reject ride with ID: {ride_id}")
        # Get the current user
        from ..crud import get_user_by_email, get_ride, update_ride_status
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        print(f"User found: {user.email}")
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        print(f"Driver found: {driver.name} with ID: {driver.id}")
        # Get the ride
        ride = get_ride(ride_id)
        if not ride:
            print(f"Ride with ID {ride_id} not found in database")
            raise HTTPException(status_code=404, detail="Ride not found")
            
        print(f"Ride found: {ride.id} with driver ID: {ride.driver_id} and status: {ride.status}")
        # Verify that this ride is assigned to the current driver
        if str(ride.driver_id) != str(driver.id):
            raise HTTPException(status_code=403, detail="This ride is not assigned to you")
            
        # Verify that the ride is in 'assigned' status
        if ride.status != "assigned":
            raise HTTPException(status_code=400, detail=f"Ride is in {ride.status} status and cannot be rejected")
            
        # Update ride status to 'rejected'
        updated_ride = update_ride_status(ride_id, "rejected")
        if not updated_ride:
            raise HTTPException(status_code=500, detail="Error updating ride status")
            
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(updated_ride.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in reject_ride: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error rejecting ride: {str(e)}")

@router.post("/me/rides/{ride_id}/start")
async def start_ride(ride_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Start a ride as the currently authenticated driver
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email, get_ride, update_ride_status
        from datetime import datetime
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        # Get the ride
        ride = get_ride(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
            
        # Verify that this ride is assigned to the current driver
        if str(ride.driver_id) != str(driver.id):
            raise HTTPException(status_code=403, detail="This ride is not assigned to you")
            
        # Verify that the ride is in 'accepted' status
        if ride.status != "accepted":
            raise HTTPException(status_code=400, detail=f"Ride is in {ride.status} status and cannot be started. Only accepted rides can be started.")
            
        # Update ride status to 'started' and set start time
        from ..crud import update_ride
        from ..schemas import RideCreate
        updated_ride_data = RideCreate(
            user_id=ride.user_id,
            rider_id=ride.rider_id,
            driver_id=ride.driver_id,
            algorithm=ride.algorithm,
            start_time=datetime.now(),
            end_time=ride.end_time,
            fare=ride.fare,
            utility=ride.utility,
            status="started"
        )
        
        updated_ride = update_ride(ride_id, updated_ride_data)
        if not updated_ride:
            raise HTTPException(status_code=500, detail="Error updating ride status")
            
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(updated_ride.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in start_ride: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error starting ride: {str(e)}")

@router.post("/me/rides/{ride_id}/end")
async def end_ride(ride_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    End a ride as the currently authenticated driver
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email, get_ride, update_ride
        from datetime import datetime
        from ..schemas import RideCreate
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get driver by user ID
        driver = get_driver_by_user_id(user.id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver profile not found")
            
        # Get the ride
        ride = get_ride(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
            
        # Verify that this ride is assigned to the current driver
        if str(ride.driver_id) != str(driver.id):
            raise HTTPException(status_code=403, detail="This ride is not assigned to you")
            
        # Verify that the ride is in 'started' status
        if ride.status != "started":
            raise HTTPException(status_code=400, detail=f"Ride is in {ride.status} status and cannot be ended. Only started rides can be ended.")
            
        # Update ride status to 'completed' and set end time
        updated_ride_data = RideCreate(
            user_id=ride.user_id,
            rider_id=ride.rider_id,
            driver_id=ride.driver_id,
            algorithm=ride.algorithm,
            start_time=ride.start_time,
            end_time=datetime.now(),
            fare=ride.fare,
            utility=ride.utility,
            status="completed"
        )
        
        updated_ride = update_ride(ride_id, updated_ride_data)
        if not updated_ride:
            raise HTTPException(status_code=500, detail="Error updating ride status")
            
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(updated_ride.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in end_ride: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error ending ride: {str(e)}")

@router.post("/{driver_id}/location")
async def update_location(driver_id: UUID, location: DriverUpdateLocation, current_user_email: str = Depends(get_current_user)):
    """
    Update driver location and availability
    """
    try:
        # Get the current user
        from ..crud import get_user_by_email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify the driver belongs to the authenticated user
        # In a real implementation, you would check if the user is authorized to update this driver's location
        # For now, we'll just process the request
        
        driver = update_driver_location(
            driver_id, 
            location.current_lat, 
            location.current_lon, 
            location.available if location.available is not None else True
        )
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler({"message": "Location updated successfully"})
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in update_location: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating driver location: {str(e)}")

@router.get("/{driver_id}/rides")
async def get_driver_rides(driver_id: UUID):
    """
    Get all rides for a specific driver by driver ID
    """
    try:
        # Check if driver exists
        driver = get_driver(driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        # Get all rides for this driver
        rides = get_rides_by_driver(driver_id)
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([ride.dict() for ride in rides])
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_driver_rides: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving rides: {str(e)}")

@router.get("/{driver_id}/notifications")
async def get_driver_notifications(driver_id: UUID):
    """
    Get notifications for a specific driver
    """
    try:
        driver = get_driver(driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
            
        notifications = get_user_notifications(driver_id)
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler([notification.dict() for notification in notifications])
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_driver_notifications: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving notifications: {str(e)}")

@router.post("/{driver_id}/notifications/{notification_id}/read")
async def mark_notification_read(driver_id: UUID, notification_id: UUID):
    """
    Mark a notification as read
    """
    try:
        driver = get_driver(driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
            
        notification = mark_notification_as_read(notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(notification.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in mark_notification_read: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error marking notification as read: {str(e)}")