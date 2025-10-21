from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List
from ..crud import get_user_notifications, mark_notification_as_read, create_notification, get_user_by_email
from ..schemas import NotificationCreate, NotificationResponse
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/user")
async def get_user_notifications_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Retrieve notifications for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get all notifications for this user
        notifications = get_user_notifications(user.id)
        
        return simple_datetime_handler([notification.dict() for notification in notifications])
    except Exception as e:
        print(f"Error in get_user_notifications_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving notifications: {str(e)}")

@router.post("/{notification_id}/read")
async def mark_notification_as_read_endpoint(notification_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Mark a notification as read for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # In a real implementation, you would verify the user owns this notification
        # Mark the notification as read
        notification = mark_notification_as_read(notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        response = {
            "message": "Notification marked as read",
            "notification": notification.dict()
        }
        
        return simple_datetime_handler(response)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in mark_notification_as_read_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error marking notification as read: {str(e)}")

@router.post("/", response_model=NotificationResponse)
async def create_notification_endpoint(notification: NotificationCreate, current_user_email: str = Depends(get_current_user)):
    """
    Create a new notification for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use the authenticated user's ID
        notification_data = notification.model_copy(update={"user_id": user.id})
        
        # Create the notification in the database
        notification_response = create_notification(notification_data)
        
        return simple_datetime_handler(notification_response)
    except Exception as e:
        print(f"Error in create_notification_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating notification: {str(e)}")