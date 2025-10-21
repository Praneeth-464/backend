from fastapi import APIRouter, HTTPException, Query, Depends
from uuid import UUID
from ..schemas import ChatMessageCreate, ChatMessageResponse
from ..crud import create_chat_message, get_chat_messages, mark_message_as_read, get_user_by_email
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.post("/", response_model=ChatMessageResponse)
async def create_chat_message_endpoint(
    message: ChatMessageCreate,
    current_user_email: str = Depends(get_current_user)
):
    """
    Create a chat message for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Determine sender type based on user's role
        # In a real implementation, you would check if the user is a rider or driver
        # for the specific ride they're trying to chat about
        sender_type = "rider"  # Default assumption
        
        # Note: In a real implementation, you would validate that the user
        # is authorized to send messages for this ride
        chat_message = create_chat_message(
            message.ride_id,
            user.id,
            sender_type,
            message.message
        )
        
        if not chat_message:
            raise HTTPException(status_code=500, detail="Error creating chat message")
        
        return simple_datetime_handler(chat_message)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_chat_message_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating chat message: {str(e)}")

@router.get("/{ride_id}", response_model=list[ChatMessageResponse])
async def get_chat_messages_endpoint(ride_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Get all chat messages for a ride (authenticated user only)
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # In a real implementation, you would verify the user has access to this ride
        messages = get_chat_messages(ride_id)
        return simple_datetime_handler(messages)
    except Exception as e:
        print(f"Error in get_chat_messages_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving chat messages: {str(e)}")

@router.post("/{message_id}/read", response_model=ChatMessageResponse)
async def mark_message_as_read_endpoint(message_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Mark a chat message as read (authenticated user only)
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # In a real implementation, you would verify the user has access to this message
        message = mark_message_as_read(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return simple_datetime_handler(message)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in mark_message_as_read_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error marking message as read: {str(e)}")