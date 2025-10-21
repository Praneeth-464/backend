from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from ..schemas import MatchRequest, MatchResponse
from ..algorithms.rga import rga_algorithm
from ..algorithms.rga_plus import rga_plus_algorithm
from ..algorithms.rga_enhanced import rga_enhanced_algorithm
from ..algorithms.iterative_voting import iterative_voting_algorithm
from ..crud import create_ride, get_user_by_email
from ..sendgrid_client import send_email_sync
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.post("/run")
async def run_matching_algorithm(request: MatchRequest, background_tasks: BackgroundTasks, current_user_email: str = Depends(get_current_user)):
    """
    Run selected algorithm (RGA/RGA++/IV) for ride matching
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if request.algorithm == "RGA":
            result = rga_algorithm()
        elif request.algorithm == "RGA++":
            result = rga_plus_algorithm()
        elif request.algorithm == "RGA-Enhanced":
            result = rga_enhanced_algorithm()
        elif request.algorithm == "IV":
            result = iterative_voting_algorithm()
        else:
            raise HTTPException(status_code=400, detail="Invalid algorithm specified")
        
        # Process assignments (save to database)
        for assignment in result.assignments:
            # In a full implementation, save each ride assignment to the database
            # create_ride(assignment)
            pass
        
        # Send notification emails in the background
        background_tasks.add_task(send_match_notifications, result)
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(result.dict())
        return serialized_result
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in run_matching_algorithm: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

def send_match_notifications(result: MatchResponse):
    """
    Send email notifications to riders and drivers about their assignments
    This function runs in the background
    """
    # In a full implementation, you would:
    # 1. Get rider and driver details from the database
    # 2. Send emails to each rider and driver with their match details
    # 3. Include algorithm used, utility scores, etc.
    
    # Example email sending (simplified):
    # for assignment in result.assignments:
    #     # Get rider and driver details
    #     # send_email_sync(rider_email, subject, body)
    #     # send_email_sync(driver_email, subject, body)
    #     pass
    
    print(f"Sending notifications for {len(result.assignments)} assignments using {result.algorithm}")