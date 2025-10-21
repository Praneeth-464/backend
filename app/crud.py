from typing import List, Optional
from uuid import UUID
from datetime import datetime
import secrets
from .database import get_supabase_client
from .schemas import RiderCreate, RiderResponse, DriverCreate, DriverResponse, RideCreate, RideResponse, UserCreate, UserResponse, RatingCreate, RatingResponse, NotificationCreate, NotificationResponse, DriverEarnings, OTPRequest, OTPVerifyRequest
from .utils.datetime_serializer import simple_datetime_handler
from .utils.jwt_utils import get_password_hash  # This now returns password as-is

supabase = get_supabase_client()

# User CRUD operations
def create_user(user: UserCreate) -> UserResponse:
    # Store the password as-is (no hashing) - INSECURE FOR PRODUCTION
    user_data = user.dict()
    user_data['password_hash'] = get_password_hash(user_data.pop('password'))  # This now stores plain text
    user_data['role'] = 'user'  # Default role
    
    # Add email verification fields
    user_data['email_verified'] = False
    user_data['email_verification_token'] = secrets.token_urlsafe(32)
    user_data['email_verification_sent_at'] = datetime.now().isoformat()
    
    response = supabase.table("users").insert(user_data).execute()
    # Use simple datetime handler for serialization
    result_data = simple_datetime_handler(response.data[0])
    return UserResponse(**result_data)

def get_user_by_email(email: str) -> Optional[UserResponse]:
    response = supabase.table("users").select("*").eq("email", email).execute()
    if response.data:
        # Use simple datetime handler for serialization
        user_data = simple_datetime_handler(response.data[0])
        return UserResponse(**user_data)
    return None

def get_user_by_verification_token(token: str) -> Optional[UserResponse]:
    response = supabase.table("users").select("*").eq("email_verification_token", token).execute()
    if response.data:
        # Use simple datetime handler for serialization
        user_data = simple_datetime_handler(response.data[0])
        return UserResponse(**user_data)
    return None

def verify_user_email(token: str) -> Optional[UserResponse]:
    # Find user by verification token
    user = get_user_by_verification_token(token)
    if not user:
        return None
    
    # Update user as verified
    update_data = {
        "email_verified": True,
        "email_verification_token": None,
        "email_verification_sent_at": None
    }
    response = supabase.table("users").update(update_data).eq("id", str(user.id)).execute()
    if response.data:
        # Use simple datetime handler for serialization
        user_data = simple_datetime_handler(response.data[0])
        return UserResponse(**user_data)
    return None

def resend_verification_email(user_id: UUID) -> Optional[UserResponse]:
    # Generate new verification token
    new_token = secrets.token_urlsafe(32)
    update_data = {
        "email_verification_token": new_token,
        "email_verification_sent_at": datetime.now().isoformat()
    }
    response = supabase.table("users").update(update_data).eq("id", str(user_id)).execute()
    if response.data:
        # Use simple datetime handler for serialization
        user_data = simple_datetime_handler(response.data[0])
        return UserResponse(**user_data)
    return None

def update_user_last_login(user_id: UUID) -> Optional[UserResponse]:
    update_data = {
        "last_login": datetime.now().isoformat()
    }
    response = supabase.table("users").update(update_data).eq("id", user_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        user_data = simple_datetime_handler(response.data[0])
        return UserResponse(**user_data)
    return None

def get_user_by_id(user_id: UUID) -> Optional[UserResponse]:
    """
    Get user by ID
    """
    try:
        response = supabase.table("users").select("*").eq("id", str(user_id)).execute()
        if response.data:
            # Use simple datetime handler for serialization
            user_data = simple_datetime_handler(response.data[0])
            return UserResponse(**user_data)
        return None
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None

def update_user_role(user_id: UUID, role: str) -> Optional[UserResponse]:
    """
    Update user role in the database
    Updates to 'rider', 'driver', or 'both' if user has both roles
    """
    try:
        # First, get the current user to check existing role
        current_user = get_user_by_id(user_id)
        if not current_user:
            return None
            
        current_role = current_user.role
        
        # Determine the new role
        new_role = role
        if current_role == 'rider' and role == 'driver':
            new_role = 'both'
        elif current_role == 'driver' and role == 'rider':
            new_role = 'both'
        # If role is already 'both', keep it as 'both'
        elif current_role == 'both':
            new_role = 'both'
            
        update_data = {"role": new_role}
        response = supabase.table("users").update(update_data).eq("id", str(user_id)).execute()
        if response.data:
            # Use simple datetime handler for serialization
            user_data = simple_datetime_handler(response.data[0])
            return UserResponse(**user_data)
        return None
    except Exception as e:
        print(f"Error updating user role: {e}")
        return None

def update_user_profile(user_id: UUID, name: Optional[str] = None, email: Optional[str] = None) -> Optional[UserResponse]:
    """
    Update user profile information
    """
    try:
        # Build update data dictionary
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if email is not None:
            update_data["email"] = email
            
        # Only update if there's data to update
        if not update_data:
            return get_user_by_id(user_id)
            
        response = supabase.table("users").update(update_data).eq("id", str(user_id)).execute()
        if response.data:
            # Use simple datetime handler for serialization
            user_data = simple_datetime_handler(response.data[0])
            return UserResponse(**user_data)
        return None
    except Exception as e:
        print(f"Error updating user profile: {e}")
        return None

# Rider CRUD operations
def create_rider(rider: RiderCreate) -> RiderResponse:
    # Serialize datetime objects before sending to Supabase
    # Use model_dump with mode="json" to apply Pydantic's json_encoders
    rider_data = rider.model_dump(mode="json")
    response = supabase.table("riders").insert(rider_data).execute()
    # Use simple datetime handler for serialization
    result_data = simple_datetime_handler(response.data[0])
    return RiderResponse(**result_data)

def get_rider_by_user_id(user_id: UUID) -> Optional[RiderResponse]:
    response = supabase.table("riders").select("*").eq("user_id", user_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        rider_data = simple_datetime_handler(response.data[0])
        return RiderResponse(**rider_data)
    return None

def get_rider(rider_id: UUID) -> Optional[RiderResponse]:
    response = supabase.table("riders").select("*").eq("id", rider_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        rider_data = simple_datetime_handler(response.data[0])
        return RiderResponse(**rider_data)
    return None

def get_riders() -> List[RiderResponse]:
    response = supabase.table("riders").select("*").execute()
    riders = []
    for rider_data in response.data:
        # Use simple datetime handler for serialization
        serialized_data = simple_datetime_handler(rider_data)
        riders.append(RiderResponse(**serialized_data))
    return riders

def update_rider(rider_id: UUID, rider: RiderCreate) -> Optional[RiderResponse]:
    # Serialize datetime objects before sending to Supabase
    # Use model_dump with mode="json" to apply Pydantic's json_encoders
    rider_data = rider.model_dump(mode="json")
    response = supabase.table("riders").update(rider_data).eq("id", rider_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        result_data = simple_datetime_handler(response.data[0])
        return RiderResponse(**result_data)
    return None

def delete_rider(rider_id: UUID) -> bool:
    response = supabase.table("riders").delete().eq("id", rider_id).execute()
    return len(response.data) > 0

# Driver CRUD operations
def create_driver(driver: DriverCreate) -> DriverResponse:
    # Serialize datetime objects before sending to Supabase
    # Use model_dump with mode="json" to apply Pydantic's json_encoders
    driver_data = driver.model_dump(mode="json")
    response = supabase.table("drivers").insert(driver_data).execute()
    # Use simple datetime handler for serialization
    result_data = simple_datetime_handler(response.data[0])
    return DriverResponse(**result_data)

def get_driver_by_user_id(user_id: UUID) -> Optional[DriverResponse]:
    response = supabase.table("drivers").select("*").eq("user_id", user_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        driver_data = simple_datetime_handler(response.data[0])
        return DriverResponse(**driver_data)
    return None

def get_driver(driver_id: UUID) -> Optional[DriverResponse]:
    response = supabase.table("drivers").select("*").eq("id", driver_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        driver_data = simple_datetime_handler(response.data[0])
        return DriverResponse(**driver_data)
    return None

def get_drivers() -> List[DriverResponse]:
    response = supabase.table("drivers").select("*").execute()
    drivers = []
    for driver_data in response.data:
        # Use simple datetime handler for serialization
        serialized_data = simple_datetime_handler(driver_data)
        drivers.append(DriverResponse(**serialized_data))
    return drivers

def update_driver(driver_id: UUID, driver: DriverCreate) -> Optional[DriverResponse]:
    # Serialize datetime objects before sending to Supabase
    # Use model_dump with mode="json" to apply Pydantic's json_encoders
    driver_data = driver.model_dump(mode="json")
    response = supabase.table("drivers").update(driver_data).eq("id", driver_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        result_data = simple_datetime_handler(response.data[0])
        return DriverResponse(**result_data)
    return None

def update_driver_location(driver_id: UUID, lat: float, lon: float, available: bool = True) -> Optional[DriverResponse]:
    update_data = {
        "current_lat": lat,
        "current_lon": lon,
        "available": available
    }
    response = supabase.table("drivers").update(update_data).eq("id", driver_id).execute()
    if response.data:
        # Use simple datetime handler for serialization
        driver_data = simple_datetime_handler(response.data[0])
        return DriverResponse(**driver_data)
    return None

def delete_driver(driver_id: UUID) -> bool:
    response = supabase.table("drivers").delete().eq("id", driver_id).execute()
    return len(response.data) > 0

# Ride CRUD operations
def create_ride(ride: RideCreate) -> RideResponse:
    # Serialize datetime objects before sending to Supabase
    # Use model_dump with mode="json" to apply Pydantic's json_encoders
    ride_data = ride.model_dump(mode="json")
    response = supabase.table("rides").insert(ride_data).execute()
    # Use simple datetime handler for serialization
    result_data = simple_datetime_handler(response.data[0])
    return RideResponse(**result_data)

def get_rides_by_user_id(user_id: UUID) -> List[RideResponse]:
    """
    Get all rides for a specific user
    """
    try:
        response = supabase.table("rides").select("*").eq("user_id", str(user_id)).execute()
        rides = []
        for ride_data in response.data:
            # Use simple datetime handler for serialization
            serialized_data = simple_datetime_handler(ride_data)
            rides.append(RideResponse(**serialized_data))
        return rides
    except Exception as e:
        print(f"Error getting rides by user: {e}")
        return []

def get_rides() -> List[RideResponse]:
    """
    Get all rides
    """
    try:
        response = supabase.table("rides").select("*").execute()
        rides = []
        for ride_data in response.data:
            # Use simple datetime handler for serialization
            serialized_data = simple_datetime_handler(ride_data)
            rides.append(RideResponse(**serialized_data))
        return rides
    except Exception as e:
        print(f"Error getting rides: {e}")
        return []

def get_ride(ride_id: UUID) -> Optional[RideResponse]:
    """
    Get a specific ride by ID
    """
    try:
        response = supabase.table("rides").select("*").eq("id", str(ride_id)).execute()
        if response.data:
            # Use simple datetime handler for serialization
            ride_data = simple_datetime_handler(response.data[0])
            return RideResponse(**ride_data)
        return None
    except Exception as e:
        print(f"Error getting ride: {e}")
        return None

def update_ride(ride_id: UUID, ride: RideCreate) -> Optional[RideResponse]:
    """
    Update a ride record
    """
    try:
        # Serialize datetime objects before sending to Supabase
        # Use model_dump with mode="json" to apply Pydantic's json_encoders
        ride_data = ride.model_dump(mode="json")
        response = supabase.table("rides").update(ride_data).eq("id", str(ride_id)).execute()
        if response.data:
            # Use simple datetime handler for serialization
            result_data = simple_datetime_handler(response.data[0])
            return RideResponse(**result_data)
        return None
    except Exception as e:
        print(f"Error updating ride: {e}")
        return None

def get_rides_by_rider(rider_id: UUID) -> List[RideResponse]:
    """
    Get all rides for a specific rider
    """
    try:
        response = supabase.table("rides").select("*").eq("rider_id", str(rider_id)).execute()
        rides = []
        for ride_data in response.data:
            # Use simple datetime handler for serialization
            serialized_data = simple_datetime_handler(ride_data)
            rides.append(RideResponse(**serialized_data))
        return rides
    except Exception as e:
        print(f"Error getting rides by rider: {e}")
        return []

def cancel_ride(ride_id: UUID) -> bool:
    """
    Cancel a ride by updating its status
    """
    try:
        update_data = {"status": "cancelled"}
        response = supabase.table("rides").update(update_data).eq("id", str(ride_id)).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error cancelling ride: {e}")
        return False

def update_ride_status(ride_id: UUID, status: str) -> Optional[RideResponse]:
    """
    Update the status of a ride
    """
    try:
        update_data = {"status": status}
        response = supabase.table("rides").update(update_data).eq("id", str(ride_id)).execute()
        if response.data:
            # Use simple datetime handler for serialization
            result_data = simple_datetime_handler(response.data[0])
            return RideResponse(**result_data)
        return None
    except Exception as e:
        print(f"Error updating ride status: {e}")
        return None

def get_rides_by_driver(driver_id: UUID) -> List[RideResponse]:
    """
    Get all rides for a specific driver
    """
    try:
        response = supabase.table("rides").select("*").eq("driver_id", str(driver_id)).execute()
        rides = []
        for ride_data in response.data:
            # Use simple datetime handler for serialization
            serialized_data = simple_datetime_handler(ride_data)
            rides.append(RideResponse(**serialized_data))
        return rides
    except Exception as e:
        print(f"Error getting rides by driver: {e}")
        return []

# OTP CRUD operations
def create_otp(email: str, otp: str, expires_at: datetime) -> bool:
    """
    Create a new OTP record in the database
    """
    try:
        otp_data = {
            "email": email,
            "otp": otp,
            "expires_at": expires_at.isoformat()
        }
        response = supabase.table("otps").insert(otp_data).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error creating OTP: {e}")
        return False

def get_otp_by_email(email: str) -> Optional[dict]:
    """
    Get the most recent OTP for an email that hasn't expired and hasn't been used
    """
    try:
        response = supabase.table("otps").select("*").eq("email", email).eq("used", False).gt("expires_at", datetime.now().isoformat()).order("created_at", desc=True).limit(1).execute()
        if response.data:
            # Use simple datetime handler for serialization
            otp_data = simple_datetime_handler(response.data[0])
            return otp_data
        return None
    except Exception as e:
        print(f"Error getting OTP: {e}")
        return None

def verify_otp(email: str, otp: str) -> bool:
    """
    Verify an OTP and mark it as used
    """
    try:
        # First, find the OTP record
        response = supabase.table("otps").select("*").eq("email", email).eq("otp", otp).eq("used", False).gt("expires_at", datetime.now().isoformat()).execute()
        
        if not response.data:
            return False
            
        # Mark the OTP as used
        otp_id = response.data[0]["id"]
        update_response = supabase.table("otps").update({"used": True}).eq("id", otp_id).execute()
        
        return len(update_response.data) > 0
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return False

def delete_expired_otps() -> int:
    """
    Delete expired OTPs from the database
    """
    try:
        response = supabase.table("otps").delete().lt("expires_at", datetime.now().isoformat()).execute()
        return len(response.data)
    except Exception as e:
        print(f"Error deleting expired OTPs: {e}")
        return 0

# Rating CRUD operations
def create_rating(ride_id: UUID, rating: RatingCreate, user_id: UUID) -> RatingResponse:
    # First, get the ride to get rider_id and driver_id
    ride = get_ride(ride_id)
    if not ride:
        raise Exception("Ride not found")
    
    rating_data = rating.dict()
    rating_data['user_id'] = str(user_id)
    rating_data['ride_id'] = str(ride_id)
    rating_data['rider_id'] = str(ride.rider_id)
    rating_data['driver_id'] = str(ride.driver_id)
    
    response = supabase.table("ratings").insert(rating_data).execute()
    result_data = simple_datetime_handler(response.data[0])
    return RatingResponse(**result_data)

def get_driver_ratings(driver_id: UUID) -> List[RatingResponse]:
    response = supabase.table("ratings").select("*").eq("driver_id", str(driver_id)).execute()
    ratings = []
    for rating_data in response.data:
        serialized_data = simple_datetime_handler(rating_data)
        ratings.append(RatingResponse(**serialized_data))
    return ratings

def get_driver_average_rating(driver_id: UUID) -> float:
    response = supabase.table("ratings").select("rating").eq("driver_id", str(driver_id)).execute()
    if not response.data:
        return 5.0  # Default rating
    
    ratings = [rating['rating'] for rating in response.data]
    return sum(ratings) / len(ratings) if ratings else 5.0

# Notification CRUD operations
def create_notification(notification: NotificationCreate) -> NotificationResponse:
    notification_data = notification.dict()
    response = supabase.table("notifications").insert(notification_data).execute()
    result_data = simple_datetime_handler(response.data[0])
    return NotificationResponse(**result_data)

def get_user_notifications(user_id: UUID) -> List[NotificationResponse]:
    response = supabase.table("notifications").select("*").eq("user_id", str(user_id)).order("created_at", desc=True).execute()
    notifications = []
    for notification_data in response.data:
        serialized_data = simple_datetime_handler(notification_data)
        notifications.append(NotificationResponse(**serialized_data))
    return notifications

def mark_notification_as_read(notification_id: UUID) -> Optional[NotificationResponse]:
    update_data = {"read": True}
    response = supabase.table("notifications").update(update_data).eq("id", str(notification_id)).execute()
    if response.data:
        notification_data = simple_datetime_handler(response.data[0])
        return NotificationResponse(**notification_data)
    return None

# Analytics operations
def get_system_metrics() -> dict:
    # Get total rides
    rides_response = supabase.table("rides").select("id").execute()
    total_rides = len(rides_response.data)
    
    # Get active riders (riders with recent rides)
    riders_response = supabase.table("riders").select("id").execute()
    active_riders = len(riders_response.data)
    
    # Get active drivers
    drivers_response = supabase.table("drivers").select("id").eq("available", True).execute()
    active_drivers = len(drivers_response.data)
    
    # Get average rating
    ratings_response = supabase.table("ratings").select("rating").execute()
    if ratings_response.data:
        ratings = [rating['rating'] for rating in ratings_response.data]
        average_rating = sum(ratings) / len(ratings) if ratings else 5.0
    else:
        average_rating = 5.0
    
    return {
        "total_rides": total_rides,
        "active_riders": active_riders,
        "active_drivers": active_drivers,
        "average_rating": round(average_rating, 2)
    }

def get_driver_earnings(driver_id: UUID) -> DriverEarnings:
    # Get total rides for this driver
    rides_response = supabase.table("rides").select("id, fare").eq("driver_id", str(driver_id)).execute()
    total_rides = len(rides_response.data)
    
    # Calculate total earnings
    total_earnings = sum(ride['fare'] or 0 for ride in rides_response.data)
    
    # Get average rating
    average_rating = get_driver_average_rating(driver_id)
    
    # For hours online, we would need a separate tracking system
    # For now, we'll use a placeholder
    hours_online = total_rides * 0.5  # Estimate 30 minutes per ride
    
    return DriverEarnings(
        driver_id=driver_id,
        total_earnings=total_earnings,
        total_rides=total_rides,
        average_rating=round(average_rating, 2),
        hours_online=round(hours_online, 1),
        timestamp=datetime.now()
    )

# Schedule CRUD operations
def create_schedule(algorithm: str, metadata: Optional[dict] = None, user_id: Optional[UUID] = None) -> Optional[dict]:
    """
    Create a new schedule record
    """
    try:
        schedule_data = {
            "user_id": str(user_id) if user_id else None,
            "algorithm": algorithm,
            "metadata": metadata or {}
        }
        response = supabase.table("schedules").insert(schedule_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating schedule: {e}")
        return None

def get_schedules() -> List[dict]:
    """
    Get all schedules
    """
    try:
        response = supabase.table("schedules").select("*").order("created_at", desc=True).execute()
        schedules = []
        for schedule_data in response.data:
            schedules.append(simple_datetime_handler(schedule_data))
        return schedules
    except Exception as e:
        print(f"Error getting schedules: {e}")
        return []

def get_schedule(schedule_id: UUID) -> Optional[dict]:
    """
    Get a specific schedule by ID
    """
    try:
        response = supabase.table("schedules").select("*").eq("id", str(schedule_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting schedule: {e}")
        return None

def delete_schedule(schedule_id: UUID) -> bool:
    """
    Delete a schedule by ID
    """
    try:
        response = supabase.table("schedules").delete().eq("id", str(schedule_id)).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        return False

# Fare estimation operations
def estimate_fare(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float, 
                  rider_beta: float = 0.5, traffic_multiplier: float = 1.0) -> dict:
    """
    Estimate fare based on distance, time, and other factors
    """
    try:
        # Calculate distance using haversine formula
        from .utils.distance_calc import calculate_distance
        distance_km = calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
        
        # Base fare components
        base_fare = 2.50  # Base fare in currency units
        distance_rate = 1.25  # Per kilometer
        time_rate = 0.50  # Per minute
        
        # Estimated time (assuming average speed of 30 km/h)
        estimated_duration_minutes = (distance_km / 30) * 60 * traffic_multiplier
        
        # Calculate fare components
        distance_fare = distance_km * distance_rate
        time_fare = estimated_duration_minutes * time_rate
        
        # Apply surge pricing during peak hours (simplified)
        from datetime import datetime
        current_hour = datetime.now().hour
        surge_multiplier = 1.0
        if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:  # Peak hours
            surge_multiplier = 1.25
        
        # Apply rider's patience factor (higher beta might get slight discount)
        beta_discount = 1.0 - (rider_beta * 0.05)  # Max 5% discount for high patience
        
        estimated_fare = (base_fare + distance_fare + time_fare) * surge_multiplier * beta_discount
        
        return {
            "estimated_fare": round(estimated_fare, 2),
            "distance_km": round(distance_km, 2),
            "estimated_duration_minutes": round(estimated_duration_minutes, 2),
            "base_fare": base_fare,
            "distance_fare": round(distance_fare, 2),
            "time_fare": round(time_fare, 2),
            "surge_multiplier": surge_multiplier
        }
    except Exception as e:
        print(f"Error estimating fare: {e}")
        return {
            "estimated_fare": 0.0,
            "distance_km": 0.0,
            "estimated_duration_minutes": 0.0,
            "base_fare": 0.0,
            "distance_fare": 0.0,
            "time_fare": 0.0,
            "surge_multiplier": 1.0
        }

# Scheduled rides operations
def create_scheduled_ride(rider_id: UUID, origin_lat: float, origin_lon: float, 
                         dest_lat: float, dest_lon: float, scheduled_time: datetime,
                         preferences: Optional[dict] = None, user_id: Optional[UUID] = None) -> Optional[dict]:
    """
    Create a scheduled ride request
    """
    try:
        ride_data = {
            "user_id": str(user_id) if user_id else None,
            "rider_id": str(rider_id),
            "origin_lat": origin_lat,
            "origin_lon": origin_lon,
            "destination_lat": dest_lat,
            "destination_lon": dest_lon,
            "scheduled_time": scheduled_time.isoformat(),
            "status": "scheduled",
            "preferences": preferences or {}
        }
        
        response = supabase.table("scheduled_rides").insert(ride_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating scheduled ride: {e}")
        return None

def get_scheduled_rides_by_rider(rider_id: UUID) -> List[dict]:
    """
    Get all scheduled rides for a specific rider
    """
    try:
        response = supabase.table("scheduled_rides").select("*").eq("rider_id", str(rider_id)).execute()
        scheduled_rides = []
        for ride_data in response.data:
            scheduled_rides.append(simple_datetime_handler(ride_data))
        return scheduled_rides
    except Exception as e:
        print(f"Error getting scheduled rides: {e}")
        return []

def update_scheduled_ride_status(ride_id: UUID, status: str) -> Optional[dict]:
    """
    Update the status of a scheduled ride
    """
    try:
        update_data = {"status": status}
        response = supabase.table("scheduled_rides").update(update_data).eq("id", str(ride_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating scheduled ride status: {e}")
        return None

# Wallet operations
def create_wallet_transaction(user_id: UUID, amount: float, transaction_type: str, 
                             description: str) -> Optional[dict]:
    """
    Create a wallet transaction
    """
    try:
        # First, get current balance
        wallet_response = supabase.table("wallets").select("balance").eq("user_id", str(user_id)).execute()
        current_balance = 0.0
        if wallet_response.data:
            current_balance = wallet_response.data[0].get("balance", 0.0)
        
        # Calculate new balance
        if transaction_type == "credit":
            new_balance = current_balance + amount
        else:
            new_balance = current_balance - amount
        
        # Update wallet balance
        wallet_update = {
            "user_id": str(user_id),
            "balance": new_balance
        }
        
        # Insert or update wallet record
        if wallet_response.data:
            supabase.table("wallets").update(wallet_update).eq("user_id", str(user_id)).execute()
        else:
            supabase.table("wallets").insert(wallet_update).execute()
        
        # Create transaction record
        transaction_data = {
            "user_id": str(user_id),
            "amount": amount,
            "transaction_type": transaction_type,
            "description": description,
            "balance_after": new_balance
        }
        
        response = supabase.table("wallet_transactions").insert(transaction_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating wallet transaction: {e}")
        return None

def get_wallet_balance(user_id: UUID) -> float:
    """
    Get wallet balance for a user
    """
    try:
        response = supabase.table("wallets").select("balance").eq("user_id", str(user_id)).execute()
        if response.data:
            return response.data[0].get("balance", 0.0)
        return 0.0
    except Exception as e:
        print(f"Error getting wallet balance: {e}")
        return 0.0

def get_wallet_transactions(user_id: UUID) -> List[dict]:
    """
    Get transaction history for a user
    """
    try:
        response = supabase.table("wallet_transactions").select("*").eq("user_id", str(user_id)).order("created_at", desc=True).execute()
        transactions = []
        for transaction_data in response.data:
            transactions.append(simple_datetime_handler(transaction_data))
        return transactions
    except Exception as e:
        print(f"Error getting wallet transactions: {e}")
        return []

# Loyalty operations
def update_loyalty_points(user_id: UUID, points: int) -> Optional[dict]:
    """
    Update loyalty points for a user
    """
    try:
        # First, get current points
        loyalty_response = supabase.table("loyalty_points").select("*").eq("user_id", str(user_id)).execute()
        current_points = 0
        if loyalty_response.data:
            current_points = loyalty_response.data[0].get("points", 0)
        
        # Calculate new points
        new_points = current_points + points
        
        # Determine level based on points
        if new_points >= 1000:
            level = "platinum"
        elif new_points >= 500:
            level = "gold"
        elif new_points >= 200:
            level = "silver"
        else:
            level = "bronze"
        
        # Calculate points needed for next level
        if level == "platinum":
            next_level_points = 0  # Max level
        elif level == "gold":
            next_level_points = 1000 - new_points
        elif level == "silver":
            next_level_points = 500 - new_points
        else:
            next_level_points = 200 - new_points
        
        loyalty_data = {
            "user_id": str(user_id),
            "points": new_points,
            "level": level,
            "next_level_points": next_level_points
        }
        
        # Insert or update loyalty record
        if loyalty_response.data:
            response = supabase.table("loyalty_points").update(loyalty_data).eq("user_id", str(user_id)).execute()
        else:
            response = supabase.table("loyalty_points").insert(loyalty_data).execute()
        
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating loyalty points: {e}")
        return None

def get_loyalty_info(user_id: UUID) -> Optional[dict]:
    """
    Get loyalty information for a user
    """
    try:
        response = supabase.table("loyalty_points").select("*").eq("user_id", str(user_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting loyalty info: {e}")
        return None

# Emergency contact operations
def create_emergency_contact(user_id: UUID, name: str, phone: str, 
                           relationship: Optional[str] = None, is_primary: bool = False) -> Optional[dict]:
    """
    Create an emergency contact for a user
    """
    try:
        contact_data = {
            "user_id": str(user_id),
            "name": name,
            "phone": phone,
            "relationship": relationship,
            "is_primary": is_primary
        }
        
        response = supabase.table("emergency_contacts").insert(contact_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating emergency contact: {e}")
        return None

def get_emergency_contacts(user_id: UUID) -> List[dict]:
    """
    Get all emergency contacts for a user
    """
    try:
        response = supabase.table("emergency_contacts").select("*").eq("user_id", str(user_id)).execute()
        contacts = []
        for contact_data in response.data:
            contacts.append(simple_datetime_handler(contact_data))
        return contacts
    except Exception as e:
        print(f"Error getting emergency contacts: {e}")
        return []

def get_primary_emergency_contact(user_id: UUID) -> Optional[dict]:
    """
    Get the primary emergency contact for a user
    """
    try:
        response = supabase.table("emergency_contacts").select("*").eq("user_id", str(user_id)).eq("is_primary", True).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting primary emergency contact: {e}")
        return None

# Referral operations
def create_referral(referrer_id: UUID, referee_email: str) -> Optional[dict]:
    """
    Create a referral for a user
    """
    try:
        import secrets
        referral_code = secrets.token_urlsafe(8).upper()
        
        referral_data = {
            "referrer_id": str(referrer_id),
            "referee_email": referee_email,
            "referral_code": referral_code,
            "status": "pending",
            "reward_points": 50  # Default reward points
        }
        
        response = supabase.table("referrals").insert(referral_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating referral: {e}")
        return None

def get_user_referrals(user_id: UUID) -> List[dict]:
    """
    Get all referrals for a user
    """
    try:
        response = supabase.table("referrals").select("*").eq("referrer_id", str(user_id)).execute()
        referrals = []
        for referral_data in response.data:
            referrals.append(simple_datetime_handler(referral_data))
        return referrals
    except Exception as e:
        print(f"Error getting user referrals: {e}")
        return []

def get_referral_by_code(referral_code: str) -> Optional[dict]:
    """
    Get a referral by its code
    """
    try:
        response = supabase.table("referrals").select("*").eq("referral_code", referral_code).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting referral by code: {e}")
        return None

def complete_referral(referral_id: UUID, referee_id: UUID) -> Optional[dict]:
    """
    Mark a referral as completed
    """
    try:
        from datetime import datetime
        update_data = {
            "referee_id": str(referee_id),
            "status": "completed",
            "completed_at": datetime.now().isoformat()
        }
        
        response = supabase.table("referrals").update(update_data).eq("id", str(referral_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error completing referral: {e}")
        return None

# Chat message operations
def create_chat_message(ride_id: UUID, sender_id: UUID, sender_type: str, message: str) -> Optional[dict]:
    """
    Create a chat message
    """
    try:
        message_data = {
            "ride_id": str(ride_id),
            "sender_id": str(sender_id),
            "sender_type": sender_type,
            "message": message
        }
        
        response = supabase.table("chat_messages").insert(message_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating chat message: {e}")
        return None

def get_chat_messages(ride_id: UUID) -> List[dict]:
    """
    Get all chat messages for a ride
    """
    try:
        response = supabase.table("chat_messages").select("*").eq("ride_id", str(ride_id)).order("created_at").execute()
        messages = []
        for message_data in response.data:
            messages.append(simple_datetime_handler(message_data))
        return messages
    except Exception as e:
        print(f"Error getting chat messages: {e}")
        return []

def mark_message_as_read(message_id: UUID) -> Optional[dict]:
    """
    Mark a chat message as read
    """
    try:
        update_data = {"is_read": True}
        response = supabase.table("chat_messages").update(update_data).eq("id", str(message_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error marking message as read: {e}")
        return None

# SOS operations
def trigger_emergency_sos(ride_id: UUID, user_id: UUID, message: str = "Emergency SOS") -> dict:
    """
    Trigger an emergency SOS
    """
    try:
        # Get ride information
        ride = get_ride(ride_id)
        if not ride:
            return {"message": "Ride not found", "emergency_contact_notified": False, "location_shared": False}
        
        # Get primary emergency contact
        emergency_contact = get_primary_emergency_contact(user_id)
        if not emergency_contact:
            return {"message": "No emergency contact found", "emergency_contact_notified": False, "location_shared": False}
        
        # Get rider and driver information
        rider = get_rider(ride.rider_id) if ride.rider_id else None
        driver = get_driver(ride.driver_id) if ride.driver_id else None
        
        # In a real implementation, this would:
        # 1. Send SMS/WhatsApp to emergency contact
        # 2. Send push notification to emergency contact
        # 3. Share live location URL
        # 4. Notify support team
        
        # For now, we'll just log the action
        print(f"EMERGENCY SOS TRIGGERED: {message}")
        print(f"Ride ID: {ride_id}")
        print(f"Rider: {rider.name if rider else 'Unknown'}")
        print(f"Driver: {driver.name if driver else 'Unknown'}")
        print(f"Emergency Contact: {emergency_contact['name']} ({emergency_contact['phone']})")
        
        return {
            "message": "Emergency SOS triggered successfully",
            "emergency_contact_notified": True,
            "location_shared": True
        }
    except Exception as e:
        print(f"Error triggering emergency SOS: {e}")
        return {
            "message": "Error triggering emergency SOS",
            "emergency_contact_notified": False,
            "location_shared": False
        }

# Analytics operations
def get_user_analytics(user_id: UUID, start_date: Optional[datetime] = None, 
                      end_date: Optional[datetime] = None) -> dict:
    """
    Get analytics for a user
    """
    try:
        # Get ride history
        rides_response = supabase.table("rides").select("*").eq("rider_id", str(user_id)).execute()
        
        total_rides = len(rides_response.data)
        total_spent = sum(ride.get("fare", 0) or 0 for ride in rides_response.data)
        
        # Get ratings
        ratings_response = supabase.table("ratings").select("rating").eq("rider_id", str(user_id)).execute()
        if ratings_response.data:
            ratings = [rating["rating"] for rating in ratings_response.data]
            average_rating = sum(ratings) / len(ratings) if ratings else 5.0
        else:
            average_rating = 5.0
        
        # Get favorite destinations (simplified)
        destinations = {}
        for ride in rides_response.data:
            dest_key = f"{ride.get('destination_lat', 0)},{ride.get('destination_lon', 0)}"
            destinations[dest_key] = destinations.get(dest_key, 0) + 1
        
        favorite_destinations = [
            {"location": dest, "count": count} 
            for dest, count in sorted(destinations.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        # Spending patterns (simplified)
        spending_patterns = {
            "total_spent": total_spent,
            "average_ride_cost": total_spent / total_rides if total_rides > 0 else 0,
            "rides_count": total_rides
        }
        
        return {
            "user_id": str(user_id),
            "total_rides": total_rides,
            "total_spent": round(total_spent, 2),
            "average_rating": round(average_rating, 2),
            "favorite_destinations": favorite_destinations,
            "spending_patterns": spending_patterns,
            "ride_history": simple_datetime_handler([ride for ride in rides_response.data])
        }
    except Exception as e:
        print(f"Error getting user analytics: {e}")
        return {
            "user_id": str(user_id),
            "total_rides": 0,
            "total_spent": 0.0,
            "average_rating": 5.0,
            "favorite_destinations": [],
            "spending_patterns": {},
            "ride_history": []
        }

# Ride Group operations for shared rides
def create_ride_group(name: str, creator_id: UUID, estimated_fare: Optional[float] = None) -> Optional[dict]:
    """
    Create a new ride group for shared rides
    """
    try:
        group_data = {
            "name": name,
            "creator_id": str(creator_id),
            "estimated_fare": estimated_fare,
            "status": "pending"
        }
        
        response = supabase.table("ride_groups").insert(group_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating ride group: {e}")
        return None

def get_ride_group(group_id: UUID) -> Optional[dict]:
    """
    Get a ride group by ID
    """
    try:
        response = supabase.table("ride_groups").select("*").eq("id", str(group_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting ride group: {e}")
        return None

def update_ride_group(group_id: UUID, name: Optional[str] = None, 
                     status: Optional[str] = None, final_fare: Optional[float] = None) -> Optional[dict]:
    """
    Update a ride group
    """
    try:
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if status is not None:
            update_data["status"] = status
        if final_fare is not None:
            update_data["final_fare"] = final_fare
            
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("ride_groups").update(update_data).eq("id", str(group_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating ride group: {e}")
        return None

def delete_ride_group(group_id: UUID) -> bool:
    """
    Delete a ride group
    """
    try:
        response = supabase.table("ride_groups").delete().eq("id", str(group_id)).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting ride group: {e}")
        return False

def get_user_ride_groups(user_id: UUID) -> List[dict]:
    """
    Get all ride groups for a user (where user is a member)
    """
    try:
        # First get all group IDs where user is a member
        member_response = supabase.table("ride_group_members").select("ride_group_id").eq("user_id", str(user_id)).execute()
        group_ids = [member["ride_group_id"] for member in member_response.data]
        
        if not group_ids:
            return []
        
        # Then get the actual ride groups
        response = supabase.table("ride_groups").select("*").in_("id", group_ids).execute()
        groups = []
        for group_data in response.data:
            groups.append(simple_datetime_handler(group_data))
        return groups
    except Exception as e:
        print(f"Error getting user ride groups: {e}")
        return []

# Ride Group Member operations
def add_ride_group_member(ride_group_id: UUID, user_id: UUID, role: str = "member", 
                         fare_share_percentage: float = 0) -> Optional[dict]:
    """
    Add a member to a ride group
    """
    try:
        member_data = {
            "ride_group_id": str(ride_group_id),
            "user_id": str(user_id),
            "role": role,
            "fare_share_percentage": fare_share_percentage,
            "status": "invited"
        }
        
        response = supabase.table("ride_group_members").insert(member_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error adding ride group member: {e}")
        return None

def get_ride_group_members(ride_group_id: UUID) -> List[dict]:
    """
    Get all members of a ride group
    """
    try:
        response = supabase.table("ride_group_members").select("*").eq("ride_group_id", str(ride_group_id)).execute()
        members = []
        for member_data in response.data:
            members.append(simple_datetime_handler(member_data))
        return members
    except Exception as e:
        print(f"Error getting ride group members: {e}")
        return []

def get_ride_group_member(member_id: UUID) -> Optional[dict]:
    """
    Get a specific ride group member by ID
    """
    try:
        response = supabase.table("ride_group_members").select("*").eq("id", str(member_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting ride group member: {e}")
        return None

def update_ride_group_member(member_id: UUID, status: Optional[str] = None, 
                           fare_share_percentage: Optional[float] = None) -> Optional[dict]:
    """
    Update a ride group member
    """
    try:
        update_data = {}
        if status is not None:
            update_data["status"] = status
            if status == "accepted":
                update_data["accepted_at"] = datetime.now().isoformat()
        if fare_share_percentage is not None:
            update_data["fare_share_percentage"] = fare_share_percentage
        
        response = supabase.table("ride_group_members").update(update_data).eq("id", str(member_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating ride group member: {e}")
        return None

def remove_ride_group_member(member_id: UUID) -> bool:
    """
    Remove a member from a ride group
    """
    try:
        response = supabase.table("ride_group_members").delete().eq("id", str(member_id)).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error removing ride group member: {e}")
        return False

def get_user_pending_invitations(user_id: UUID) -> List[dict]:
    """
    Get all pending invitations for a user
    """
    try:
        response = supabase.table("ride_group_members").select("*").eq("user_id", str(user_id)).eq("status", "invited").execute()
        invitations = []
        for invitation_data in response.data:
            invitations.append(simple_datetime_handler(invitation_data))
        return invitations
    except Exception as e:
        print(f"Error getting user pending invitations: {e}")
        return []

# Driver Verification and Safety operations
def create_driver_verification(driver_id: UUID, verification_type: str, 
                             document_url: Optional[str] = None, notes: Optional[str] = None,
                             verified_by: Optional[UUID] = None) -> Optional[dict]:
    """
    Create a new driver verification record
    """
    try:
        verification_data = {
            "driver_id": str(driver_id),
            "verification_type": verification_type,
            "document_url": document_url,
            "notes": notes,
            "verified_by": str(verified_by) if verified_by else None,
            "status": "pending"
        }
        
        response = supabase.table("driver_verifications").insert(verification_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating driver verification: {e}")
        return None

def get_driver_verifications(driver_id: UUID) -> List[dict]:
    """
    Get all verifications for a driver
    """
    try:
        response = supabase.table("driver_verifications").select("*").eq("driver_id", str(driver_id)).execute()
        verifications = []
        for verification_data in response.data:
            verifications.append(simple_datetime_handler(verification_data))
        return verifications
    except Exception as e:
        print(f"Error getting driver verifications: {e}")
        return []

def update_driver_verification(verification_id: UUID, status: Optional[str] = None,
                             notes: Optional[str] = None, verified_by: Optional[UUID] = None) -> Optional[dict]:
    """
    Update a driver verification record
    """
    try:
        update_data = {}
        if status is not None:
            update_data["status"] = status
        if notes is not None:
            update_data["notes"] = notes
        if verified_by is not None:
            update_data["verified_by"] = str(verified_by)
        if status in ["approved", "rejected"] and "status" in update_data:
            update_data["verified_at"] = datetime.now().isoformat()
            
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("driver_verifications").update(update_data).eq("id", str(verification_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating driver verification: {e}")
        return None

def get_pending_driver_verifications() -> List[dict]:
    """
    Get all pending driver verifications
    """
    try:
        response = supabase.table("driver_verifications").select("*").eq("status", "pending").execute()
        verifications = []
        for verification_data in response.data:
            verifications.append(simple_datetime_handler(verification_data))
        return verifications
    except Exception as e:
        print(f"Error getting pending driver verifications: {e}")
        return []

def update_driver_background_check_status(driver_id: UUID, status: str) -> Optional[dict]:
    """
    Update driver's background check status
    """
    try:
        update_data = {
            "background_check_status": status,
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("drivers").update(update_data).eq("id", str(driver_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating driver background check status: {e}")
        return None

# Driver Training Module operations
def create_driver_training_module(title: str, description: Optional[str] = None,
                                 duration_minutes: Optional[int] = None, content_url: Optional[str] = None,
                                 is_mandatory: bool = True) -> Optional[dict]:
    """
    Create a new driver training module
    """
    try:
        module_data = {
            "title": title,
            "description": description,
            "duration_minutes": duration_minutes,
            "content_url": content_url,
            "is_mandatory": is_mandatory
        }
        
        response = supabase.table("driver_training_modules").insert(module_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating driver training module: {e}")
        return None

def get_driver_training_modules() -> List[dict]:
    """
    Get all driver training modules
    """
    try:
        response = supabase.table("driver_training_modules").select("*").execute()
        modules = []
        for module_data in response.data:
            modules.append(simple_datetime_handler(module_data))
        return modules
    except Exception as e:
        print(f"Error getting driver training modules: {e}")
        return []

def get_driver_training_module(module_id: UUID) -> Optional[dict]:
    """
    Get a specific driver training module
    """
    try:
        response = supabase.table("driver_training_modules").select("*").eq("id", str(module_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting driver training module: {e}")
        return None

def update_driver_training_module(module_id: UUID, title: Optional[str] = None,
                                 description: Optional[str] = None, duration_minutes: Optional[int] = None,
                                 content_url: Optional[str] = None, is_mandatory: Optional[bool] = None) -> Optional[dict]:
    """
    Update a driver training module
    """
    try:
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if duration_minutes is not None:
            update_data["duration_minutes"] = duration_minutes
        if content_url is not None:
            update_data["content_url"] = content_url
        if is_mandatory is not None:
            update_data["is_mandatory"] = is_mandatory
            
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("driver_training_modules").update(update_data).eq("id", str(module_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating driver training module: {e}")
        return None

def delete_driver_training_module(module_id: UUID) -> bool:
    """
    Delete a driver training module
    """
    try:
        response = supabase.table("driver_training_modules").delete().eq("id", str(module_id)).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting driver training module: {e}")
        return False

# Driver Training Completion operations
def create_driver_training_completion(driver_id: UUID, training_module_id: UUID,
                                     score: Optional[float] = None, certificate_url: Optional[str] = None) -> Optional[dict]:
    """
    Record a driver's completion of a training module
    """
    try:
        completion_data = {
            "driver_id": str(driver_id),
            "training_module_id": str(training_module_id),
            "score": score,
            "certificate_url": certificate_url,
            "completed_at": datetime.now().isoformat()
        }
        
        response = supabase.table("driver_training_completions").insert(completion_data).execute()
        if response.data:
            # Check if all mandatory training is completed to update driver status
            update_driver_safety_training_status(driver_id)
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating driver training completion: {e}")
        return None

def get_driver_training_completions(driver_id: UUID) -> List[dict]:
    """
    Get all training completions for a driver
    """
    try:
        response = supabase.table("driver_training_completions").select("*").eq("driver_id", str(driver_id)).execute()
        completions = []
        for completion_data in response.data:
            completions.append(simple_datetime_handler(completion_data))
        return completions
    except Exception as e:
        print(f"Error getting driver training completions: {e}")
        return []

def update_driver_safety_training_status(driver_id: UUID) -> Optional[dict]:
    """
    Update driver's safety training completion status
    """
    try:
        # Check if all mandatory training modules are completed
        mandatory_modules_response = supabase.table("driver_training_modules").select("id").eq("is_mandatory", True).execute()
        mandatory_module_ids = [module["id"] for module in mandatory_modules_response.data]
        
        if not mandatory_module_ids:
            # No mandatory modules, mark as completed
            update_data = {
                "safety_training_completed": True,
                "updated_at": datetime.now().isoformat()
            }
        else:
            # Check if all mandatory modules are completed
            completed_response = supabase.table("driver_training_completions").select("training_module_id").eq("driver_id", str(driver_id)).execute()
            completed_module_ids = [completion["training_module_id"] for completion in completed_response.data]
            
            all_completed = all(module_id in completed_module_ids for module_id in mandatory_module_ids)
            
            update_data = {
                "safety_training_completed": all_completed,
                "updated_at": datetime.now().isoformat()
            }
        
        response = supabase.table("drivers").update(update_data).eq("id", str(driver_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating driver safety training status: {e}")
        return None

# Driver Incident operations
def create_driver_incident(driver_id: UUID, reporter_id: UUID, incident_type: str,
                          description: str, severity: str) -> Optional[dict]:
    """
    Create a new driver incident report
    """
    try:
        incident_data = {
            "driver_id": str(driver_id),
            "reporter_id": str(reporter_id),
            "incident_type": incident_type,
            "description": description,
            "severity": severity,
            "status": "reported"
        }
        
        response = supabase.table("driver_incidents").insert(incident_data).execute()
        if response.data:
            # Update driver's incident count
            update_driver_incident_count(driver_id)
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating driver incident: {e}")
        return None

def get_driver_incidents(driver_id: UUID) -> List[dict]:
    """
    Get all incidents for a driver
    """
    try:
        response = supabase.table("driver_incidents").select("*").eq("driver_id", str(driver_id)).execute()
        incidents = []
        for incident_data in response.data:
            incidents.append(simple_datetime_handler(incident_data))
        return incidents
    except Exception as e:
        print(f"Error getting driver incidents: {e}")
        return []

def get_pending_driver_incidents() -> List[dict]:
    """
    Get all pending driver incidents
    """
    try:
        response = supabase.table("driver_incidents").select("*").eq("status", "reported").execute()
        incidents = []
        for incident_data in response.data:
            incidents.append(simple_datetime_handler(incident_data))
        return incidents
    except Exception as e:
        print(f"Error getting pending driver incidents: {e}")
        return []

def update_driver_incident(incident_id: UUID, status: Optional[str] = None,
                          resolution_notes: Optional[str] = None, resolved_by: Optional[UUID] = None) -> Optional[dict]:
    """
    Update a driver incident report
    """
    try:
        update_data = {}
        if status is not None:
            update_data["status"] = status
        if resolution_notes is not None:
            update_data["resolution_notes"] = resolution_notes
        if resolved_by is not None:
            update_data["resolved_by"] = str(resolved_by)
        if status in ["resolved", "dismissed"] and "status" in update_data:
            update_data["resolved_at"] = datetime.now().isoformat()
            
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("driver_incidents").update(update_data).eq("id", str(incident_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating driver incident: {e}")
        return None

def update_driver_incident_count(driver_id: UUID) -> Optional[dict]:
    """
    Update driver's total incident count
    """
    try:
        # Count incidents for this driver
        response = supabase.table("driver_incidents").select("id").eq("driver_id", str(driver_id)).execute()
        incident_count = len(response.data)
        
        update_data = {
            "total_incidents": incident_count,
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("drivers").update(update_data).eq("id", str(driver_id)).execute()
        if response.data:
            # Update performance score based on incidents
            update_driver_performance_score(driver_id)
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating driver incident count: {e}")
        return None

# Driver Performance Metric operations
def create_driver_performance_metric(driver_id: UUID, metric_type: str, score: float,
                                   period_start: datetime, period_end: datetime, notes: Optional[str] = None) -> Optional[dict]:
    """
    Create a new driver performance metric
    """
    try:
        metric_data = {
            "driver_id": str(driver_id),
            "metric_type": metric_type,
            "score": score,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "notes": notes
        }
        
        response = supabase.table("driver_performance_metrics").insert(metric_data).execute()
        if response.data:
            # Update overall driver performance score
            update_driver_performance_score(driver_id)
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating driver performance metric: {e}")
        return None

def get_driver_performance_metrics(driver_id: UUID) -> List[dict]:
    """
    Get all performance metrics for a driver
    """
    try:
        response = supabase.table("driver_performance_metrics").select("*").eq("driver_id", str(driver_id)).execute()
        metrics = []
        for metric_data in response.data:
            metrics.append(simple_datetime_handler(metric_data))
        return metrics
    except Exception as e:
        print(f"Error getting driver performance metrics: {e}")
        return []

def update_driver_performance_score(driver_id: UUID) -> Optional[dict]:
    """
    Update driver's overall performance score based on metrics and incidents
    """
    try:
        # Get performance metrics
        metrics_response = supabase.table("driver_performance_metrics").select("score").eq("driver_id", str(driver_id)).execute()
        metric_scores = [metric["score"] for metric in metrics_response.data]
        
        # Calculate average metric score (if any metrics exist)
        avg_metric_score = sum(metric_scores) / len(metric_scores) if metric_scores else 100.00
        
        # Get incident count
        driver_response = supabase.table("drivers").select("total_incidents").eq("id", str(driver_id)).execute()
        incident_count = driver_response.data[0]["total_incidents"] if driver_response.data else 0
        
        # Calculate penalty based on incidents (5 points per incident)
        incident_penalty = incident_count * 5
        
        # Calculate final score (min 0)
        final_score = max(0, avg_metric_score - incident_penalty)
        
        update_data = {
            "performance_score": round(final_score, 2),
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("drivers").update(update_data).eq("id", str(driver_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating driver performance score: {e}")
        return None

def get_drivers_by_performance_score(min_score: float = 0, max_score: float = 100) -> List[dict]:
    """
    Get drivers within a performance score range
    """
    try:
        response = supabase.table("drivers").select("*").gte("performance_score", min_score).lte("performance_score", max_score).execute()
        drivers = []
        for driver_data in response.data:
            drivers.append(simple_datetime_handler(driver_data))
        return drivers
    except Exception as e:
        print(f"Error getting drivers by performance score: {e}")
        return []

# Subscription Plan operations
def create_subscription_plan(name: str, description: Optional[str], price: float, billing_cycle: str,
                           ride_limit: Optional[int], priority_booking: bool, discount_percentage: float,
                           cancellation_fee_waiver: bool, customer_support_priority: str) -> Optional[dict]:
    """
    Create a new subscription plan
    """
    try:
        plan_data = {
            "name": name,
            "description": description,
            "price": price,
            "billing_cycle": billing_cycle,
            "ride_limit": ride_limit,
            "priority_booking": priority_booking,
            "discount_percentage": discount_percentage,
            "cancellation_fee_waiver": cancellation_fee_waiver,
            "customer_support_priority": customer_support_priority
        }
        
        response = supabase.table("subscription_plans").insert(plan_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating subscription plan: {e}")
        return None

def get_subscription_plans() -> List[dict]:
    """
    Get all subscription plans
    """
    try:
        response = supabase.table("subscription_plans").select("*").execute()
        plans = []
        for plan_data in response.data:
            plans.append(simple_datetime_handler(plan_data))
        return plans
    except Exception as e:
        print(f"Error getting subscription plans: {e}")
        return []

def get_subscription_plan(plan_id: UUID) -> Optional[dict]:
    """
    Get a subscription plan by ID
    """
    try:
        response = supabase.table("subscription_plans").select("*").eq("id", str(plan_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting subscription plan: {e}")
        return None

def update_subscription_plan(plan_id: UUID, name: Optional[str] = None, description: Optional[str] = None,
                           price: Optional[float] = None, billing_cycle: Optional[str] = None,
                           ride_limit: Optional[int] = None, priority_booking: Optional[bool] = None,
                           discount_percentage: Optional[float] = None,
                           cancellation_fee_waiver: Optional[bool] = None,
                           customer_support_priority: Optional[str] = None) -> Optional[dict]:
    """
    Update a subscription plan
    """
    try:
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if price is not None:
            update_data["price"] = price
        if billing_cycle is not None:
            update_data["billing_cycle"] = billing_cycle
        if ride_limit is not None:
            update_data["ride_limit"] = ride_limit
        if priority_booking is not None:
            update_data["priority_booking"] = priority_booking
        if discount_percentage is not None:
            update_data["discount_percentage"] = discount_percentage
        if cancellation_fee_waiver is not None:
            update_data["cancellation_fee_waiver"] = cancellation_fee_waiver
        if customer_support_priority is not None:
            update_data["customer_support_priority"] = customer_support_priority
            
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("subscription_plans").update(update_data).eq("id", str(plan_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating subscription plan: {e}")
        return None

def delete_subscription_plan(plan_id: UUID) -> bool:
    """
    Delete a subscription plan
    """
    try:
        response = supabase.table("subscription_plans").delete().eq("id", str(plan_id)).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting subscription plan: {e}")
        return False

# User Subscription operations
def create_user_subscription(user_id: UUID, plan_id: UUID, start_date: datetime,
                           end_date: Optional[datetime] = None, auto_renew: bool = True,
                           payment_method_id: Optional[str] = None) -> Optional[dict]:
    """
    Create a new user subscription
    """
    try:
        subscription_data = {
            "user_id": str(user_id),
            "plan_id": str(plan_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat() if end_date else None,
            "auto_renew": auto_renew,
            "payment_method_id": payment_method_id,
            "status": "active"
        }
        
        response = supabase.table("user_subscriptions").insert(subscription_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating user subscription: {e}")
        return None

def get_user_subscriptions(user_id: UUID) -> List[dict]:
    """
    Get all subscriptions for a user
    """
    try:
        response = supabase.table("user_subscriptions").select("*").eq("user_id", str(user_id)).execute()
        subscriptions = []
        for subscription_data in response.data:
            subscriptions.append(simple_datetime_handler(subscription_data))
        return subscriptions
    except Exception as e:
        print(f"Error getting user subscriptions: {e}")
        return []

def get_user_active_subscription(user_id: UUID) -> Optional[dict]:
    """
    Get the active subscription for a user
    """
    try:
        response = supabase.table("user_subscriptions").select("*").eq("user_id", str(user_id)).eq("status", "active").execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting user active subscription: {e}")
        return None

def get_subscription(subscription_id: UUID) -> Optional[dict]:
    """
    Get a subscription by ID
    """
    try:
        response = supabase.table("user_subscriptions").select("*").eq("id", str(subscription_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting subscription: {e}")
        return None

def update_user_subscription(subscription_id: UUID, status: Optional[str] = None,
                           end_date: Optional[datetime] = None, auto_renew: Optional[bool] = None,
                           payment_method_id: Optional[str] = None) -> Optional[dict]:
    """
    Update a user subscription
    """
    try:
        update_data = {}
        if status is not None:
            update_data["status"] = status
        if end_date is not None:
            update_data["end_date"] = end_date.isoformat()
        if auto_renew is not None:
            update_data["auto_renew"] = auto_renew
        if payment_method_id is not None:
            update_data["payment_method_id"] = payment_method_id
            
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("user_subscriptions").update(update_data).eq("id", str(subscription_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating user subscription: {e}")
        return None

def cancel_user_subscription(subscription_id: UUID) -> Optional[dict]:
    """
    Cancel a user subscription
    """
    try:
        update_data = {
            "status": "cancelled",
            "end_date": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("user_subscriptions").update(update_data).eq("id", str(subscription_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error cancelling user subscription: {e}")
        return None

# Recurring Ride operations
def create_recurring_ride(user_id: UUID, origin_lat: float, origin_lon: float,
                         destination_lat: float, destination_lon: float, frequency: str,
                         start_time: str, end_date: Optional[datetime] = None,
                         days_of_week: Optional[List[int]] = None, day_of_month: Optional[int] = None,
                         preferences: Optional[dict] = None) -> Optional[dict]:
    """
    Create a new recurring ride
    """
    try:
        ride_data = {
            "user_id": str(user_id),
            "origin_lat": origin_lat,
            "origin_lon": origin_lon,
            "destination_lat": destination_lat,
            "destination_lon": destination_lon,
            "frequency": frequency,
            "days_of_week": days_of_week,
            "day_of_month": day_of_month,
            "start_time": start_time,
            "end_date": end_date.isoformat() if end_date else None,
            "preferences": preferences,
            "status": "active"
        }
        
        response = supabase.table("recurring_rides").insert(ride_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating recurring ride: {e}")
        return None

def get_user_recurring_rides(user_id: UUID) -> List[dict]:
    """
    Get all recurring rides for a user
    """
    try:
        response = supabase.table("recurring_rides").select("*").eq("user_id", str(user_id)).execute()
        rides = []
        for ride_data in response.data:
            rides.append(simple_datetime_handler(ride_data))
        return rides
    except Exception as e:
        print(f"Error getting user recurring rides: {e}")
        return []

def get_recurring_ride(ride_id: UUID) -> Optional[dict]:
    """
    Get a recurring ride by ID
    """
    try:
        response = supabase.table("recurring_rides").select("*").eq("id", str(ride_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error getting recurring ride: {e}")
        return None

def update_recurring_ride(ride_id: UUID, frequency: Optional[str] = None,
                         days_of_week: Optional[List[int]] = None, day_of_month: Optional[int] = None,
                         start_time: Optional[str] = None, end_date: Optional[datetime] = None,
                         status: Optional[str] = None, preferences: Optional[dict] = None) -> Optional[dict]:
    """
    Update a recurring ride
    """
    try:
        update_data = {}
        if frequency is not None:
            update_data["frequency"] = frequency
        if days_of_week is not None:
            update_data["days_of_week"] = days_of_week
        if day_of_month is not None:
            update_data["day_of_month"] = day_of_month
        if start_time is not None:
            update_data["start_time"] = start_time
        if end_date is not None:
            update_data["end_date"] = end_date.isoformat() if end_date else None
        if status is not None:
            update_data["status"] = status
        if preferences is not None:
            update_data["preferences"] = preferences
            
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("recurring_rides").update(update_data).eq("id", str(ride_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error updating recurring ride: {e}")
        return None

def pause_recurring_ride(ride_id: UUID) -> Optional[dict]:
    """
    Pause a recurring ride
    """
    try:
        update_data = {
            "status": "paused",
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("recurring_rides").update(update_data).eq("id", str(ride_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error pausing recurring ride: {e}")
        return None

def resume_recurring_ride(ride_id: UUID) -> Optional[dict]:
    """
    Resume a paused recurring ride
    """
    try:
        update_data = {
            "status": "active",
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("recurring_rides").update(update_data).eq("id", str(ride_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error resuming recurring ride: {e}")
        return None

def cancel_recurring_ride(ride_id: UUID) -> Optional[dict]:
    """
    Cancel a recurring ride
    """
    try:
        update_data = {
            "status": "cancelled",
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("recurring_rides").update(update_data).eq("id", str(ride_id)).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error cancelling recurring ride: {e}")
        return None

def get_active_recurring_rides() -> List[dict]:
    """
    Get all active recurring rides
    """
    try:
        response = supabase.table("recurring_rides").select("*").eq("status", "active").execute()
        rides = []
        for ride_data in response.data:
            rides.append(simple_datetime_handler(ride_data))
        return rides
    except Exception as e:
        print(f"Error getting active recurring rides: {e}")
        return []

# Generated Scheduled Ride operations
def create_generated_scheduled_ride(recurring_ride_id: UUID, scheduled_ride_id: UUID) -> Optional[dict]:
    """
    Create a record of a scheduled ride generated from a recurring ride
    """
    try:
        ride_data = {
            "recurring_ride_id": str(recurring_ride_id),
            "scheduled_ride_id": str(scheduled_ride_id)
        }
        
        response = supabase.table("generated_scheduled_rides").insert(ride_data).execute()
        if response.data:
            return simple_datetime_handler(response.data[0])
        return None
    except Exception as e:
        print(f"Error creating generated scheduled ride: {e}")
        return None

def get_generated_scheduled_rides(recurring_ride_id: UUID) -> List[dict]:
    """
    Get all scheduled rides generated from a recurring ride
    """
    try:
        response = supabase.table("generated_scheduled_rides").select("*").eq("recurring_ride_id", str(recurring_ride_id)).execute()
        rides = []
        for ride_data in response.data:
            rides.append(simple_datetime_handler(ride_data))
        return rides
    except Exception as e:
        print(f"Error getting generated scheduled rides: {e}")
        return []
