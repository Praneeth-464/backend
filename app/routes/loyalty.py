from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from ..schemas import LoyaltyPoints
from ..crud import update_loyalty_points, get_loyalty_info, get_user_by_email
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.get("/", response_model=LoyaltyPoints)
async def get_loyalty_info_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Get loyalty information for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        loyalty_info = get_loyalty_info(user.id)
        if not loyalty_info:
            # Return default loyalty info if none exists
            return {
                "user_id": str(user.id),
                "points": 0,
                "level": "bronze",
                "next_level_points": 200
            }
        
        return simple_datetime_handler(loyalty_info)
    except Exception as e:
        print(f"Error in get_loyalty_info_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving loyalty info: {str(e)}")

@router.post("/points")
async def update_loyalty_points_endpoint(points: int, current_user_email: str = Depends(get_current_user)):
    """
    Update loyalty points for the authenticated user (add or subtract)
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        loyalty_info = update_loyalty_points(user.id, points)
        if not loyalty_info:
            raise HTTPException(status_code=500, detail="Error updating loyalty points")
        
        return simple_datetime_handler(loyalty_info)
    except Exception as e:
        print(f"Error in update_loyalty_points_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating loyalty points: {str(e)}")