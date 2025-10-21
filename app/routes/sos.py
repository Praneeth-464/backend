from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from ..schemas import EmergencySOSRequest, EmergencySOSResponse
from ..crud import trigger_emergency_sos, get_user_by_email
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.post("/trigger", response_model=EmergencySOSResponse)
async def trigger_emergency_sos_endpoint(request: EmergencySOSRequest, current_user_email: str = Depends(get_current_user)):
    """
    Trigger an emergency SOS for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        result = trigger_emergency_sos(
            request.ride_id,
            user.id,
            request.message or "Emergency SOS"
        )
        
        return simple_datetime_handler(result)
    except Exception as e:
        print(f"Error in trigger_emergency_sos_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error triggering emergency SOS: {str(e)}")