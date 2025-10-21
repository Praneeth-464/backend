from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from ..schemas import ScheduleCreate, ScheduleResponse, MatchRequest, MatchResponse
from ..crud import create_schedule, get_schedules, get_schedule, delete_schedule, get_user_by_email
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

# Import the matching algorithms
from ..algorithms.rga import rga_algorithm
from ..algorithms.rga_plus import rga_plus_algorithm
from ..algorithms.rga_enhanced import rga_enhanced_algorithm
from ..algorithms.iterative_voting import iterative_voting_algorithm

router = APIRouter()

@router.post("/run", response_model=dict)
async def run_scheduling_algorithm(schedule_request: dict, current_user_email: str = Depends(get_current_user)):
    """
    Execute a ride matching algorithm and store the results as a schedule
    """
    try:
        # Get user from email
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Extract algorithm from request
        algorithm = schedule_request.get("algorithm", "RGA++")
        
        # Run the selected algorithm
        result = None
        if algorithm == "RGA":
            result = rga_algorithm()
        elif algorithm == "RGA++":
            result = rga_plus_algorithm()
        elif algorithm == "RGA-Enhanced":
            result = rga_enhanced_algorithm()
        elif algorithm == "IV":
            result = iterative_voting_algorithm()
        else:
            raise HTTPException(status_code=400, detail="Invalid algorithm specified")
        
        # Convert result to dict for database storage
        result_dict = result.dict()
        
        # Create schedule in database
        schedule_metadata = {
            "assignments": [assignment.dict() for assignment in result.assignments],
            "metrics": result.metrics
        }
        
        created_schedule = create_schedule(
            algorithm=algorithm,
            metadata=schedule_metadata,
            user_id=user.id
        )
        
        if not created_schedule:
            raise HTTPException(status_code=500, detail="Error creating schedule")
            
        # Return response matching API documentation
        response = {
            "algorithm": algorithm,
            "assignments": [assignment.dict() for assignment in result.assignments],
            "metrics": result.metrics,
            "schedule_id": created_schedule["id"]
        }
        
        return simple_datetime_handler(response)
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in run_scheduling_algorithm: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error running scheduling algorithm: {str(e)}")

@router.post("/", response_model=dict)
async def create_new_schedule(schedule: ScheduleCreate, current_user_email: str = Depends(get_current_user)):
    """
    Create a new schedule
    """
    try:
        # Get user from email (simplified - in a real implementation you might want to get the full user object)
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        result = create_schedule(
            algorithm=schedule.algorithm,
            metadata=schedule.metadata,
            user_id=user.id
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Error creating schedule")
            
        return simple_datetime_handler(result)
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in create_new_schedule: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
async def list_schedules():
    """
    Get all schedules
    """
    try:
        result = get_schedules()
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(result)
        return serialized_result
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in list_schedules: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving schedules: {str(e)}")

@router.get("/{schedule_id}", response_model=dict)
async def get_schedule_by_id(schedule_id: UUID):
    """
    Get a specific schedule by ID
    """
    try:
        result = get_schedule(schedule_id)
        if not result:
            raise HTTPException(status_code=404, detail="Schedule not found")
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(result)
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_schedule_by_id: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving schedule: {str(e)}")

@router.delete("/{schedule_id}")
async def delete_schedule_by_id(schedule_id: UUID):
    """
    Delete a specific schedule by ID
    """
    try:
        success = delete_schedule(schedule_id)
        if not success:
            raise HTTPException(status_code=404, detail="Schedule not found or could not be deleted")
        return {"message": "Schedule deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in delete_schedule_by_id: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error deleting schedule: {str(e)}")