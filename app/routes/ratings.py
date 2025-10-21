from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel
from ..crud import get_driver, create_rating, get_driver_ratings, get_driver_average_rating, get_ride, get_user_by_email
from ..schemas import RatingCreate, RatingResponse, DriverRatingsResponse
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/rides/{ride_id}")
async def submit_ride_rating(ride_id: UUID, rating_data: RatingCreate, current_user_email: str = Depends(get_current_user)):
    """
    Submit a rating and review for a completed ride
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate rating
        if not 1 <= rating_data.rating <= 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Create the rating in the database with user_id
        rating_response = create_rating(ride_id, rating_data, user.id)
        
        # Update driver's average rating
        ride = get_ride(ride_id)
        if ride and ride.driver_id:
            # In a real implementation, we would update the driver's average rating
            # For now, we'll just return the created rating
            pass
        
        response = {
            "message": "Rating submitted successfully",
            "rating": rating_response.dict()
        }
        
        return simple_datetime_handler(response)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in submit_ride_rating: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error submitting rating: {str(e)}")

@router.get("/drivers/{driver_id}")
async def get_driver_ratings_endpoint(driver_id: UUID):
    """
    Retrieve ratings and reviews for a specific driver
    """
    try:
        # Verify the driver exists
        driver = get_driver(driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        # Get all ratings for this driver
        ratings = get_driver_ratings(driver_id)
        
        # Calculate average rating
        average_rating = get_driver_average_rating(driver_id)
        
        ratings_response = {
            "driver_id": str(driver_id),
            "average_rating": round(average_rating, 2),
            "total_ratings": len(ratings),
            "reviews": [rating.dict() for rating in ratings]
        }
        
        return simple_datetime_handler(ratings_response)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_driver_ratings_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver ratings: {str(e)}")