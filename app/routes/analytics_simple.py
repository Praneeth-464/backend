from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from datetime import datetime
from ..schemas import AnalyticsRequest, AnalyticsResponse
from ..crud import get_user_analytics, get_user_by_email
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.post("/user", response_model=AnalyticsResponse)
async def get_user_analytics_endpoint(request: AnalyticsRequest, current_user_email: str = Depends(get_current_user)):
    """
    Get analytics for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use the authenticated user's ID
        user_id = user.id
        
        analytics = get_user_analytics(
            user_id,
            request.start_date,
            request.end_date
        )
        
        return simple_datetime_handler(analytics)
    except Exception as e:
        print(f"Error in get_user_analytics_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user analytics: {str(e)}")

@router.get("/user")
async def get_user_analytics_simple(current_user_email: str = Depends(get_current_user)):
    """
    Get analytics for the authenticated user (simple endpoint)
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        analytics = get_user_analytics(user.id)
        return simple_datetime_handler(analytics)
    except Exception as e:
        print(f"Error in get_user_analytics_simple: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user analytics: {str(e)}")