from fastapi import APIRouter, HTTPException
from uuid import UUID
from ..schemas import (
    DriverVerificationCreate, DriverVerificationUpdate, DriverVerificationResponse,
    DriverTrainingModuleCreate, DriverTrainingModuleUpdate, DriverTrainingModuleResponse,
    DriverTrainingCompletionCreate, DriverTrainingCompletionResponse,
    DriverIncidentCreate, DriverIncidentUpdate, DriverIncidentResponse,
    DriverPerformanceMetricCreate, DriverPerformanceMetricResponse
)
from ..crud import (
    create_driver_verification, get_driver_verifications, update_driver_verification, get_pending_driver_verifications,
    update_driver_background_check_status,
    create_driver_training_module, get_driver_training_modules, get_driver_training_module,
    update_driver_training_module, delete_driver_training_module,
    create_driver_training_completion, get_driver_training_completions, update_driver_safety_training_status,
    create_driver_incident, get_driver_incidents, get_pending_driver_incidents, update_driver_incident,
    update_driver_incident_count,
    create_driver_performance_metric, get_driver_performance_metrics, update_driver_performance_score,
    get_drivers_by_performance_score
)
from ..utils.datetime_serializer import simple_datetime_handler
import traceback

router = APIRouter()

# Driver Verification endpoints
@router.post("/verifications", response_model=DriverVerificationResponse)
async def create_driver_verification_endpoint(verification: DriverVerificationCreate):
    """
    Create a new driver verification record
    """
    try:
        verification_record = create_driver_verification(
            verification.driver_id,
            verification.verification_type,
            verification.document_url,
            verification.notes,
            verification.verified_by
        )
        
        if not verification_record:
            raise HTTPException(status_code=500, detail="Error creating driver verification")
        
        # If this is a background check approval, update driver status
        if verification.verification_type == "background_check" and verification_record.get("status") == "approved":
            update_driver_background_check_status(verification.driver_id, "approved")
        
        return simple_datetime_handler(verification_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_driver_verification_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating driver verification: {str(e)}")

@router.get("/verifications/{driver_id}", response_model=list[DriverVerificationResponse])
async def get_driver_verifications_endpoint(driver_id: UUID):
    """
    Get all verifications for a driver
    """
    try:
        verifications = get_driver_verifications(driver_id)
        return simple_datetime_handler(verifications)
    except Exception as e:
        print(f"Error in get_driver_verifications_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver verifications: {str(e)}")

@router.put("/verifications/{verification_id}", response_model=DriverVerificationResponse)
async def update_driver_verification_endpoint(verification_id: UUID, verification: DriverVerificationUpdate):
    """
    Update a driver verification record
    """
    try:
        verification_record = update_driver_verification(
            verification_id,
            verification.status,
            verification.notes,
            verification.verified_by
        )
        
        if not verification_record:
            raise HTTPException(status_code=404, detail="Driver verification not found")
        
        return simple_datetime_handler(verification_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_driver_verification_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating driver verification: {str(e)}")

@router.get("/verifications/pending", response_model=list[DriverVerificationResponse])
async def get_pending_driver_verifications_endpoint():
    """
    Get all pending driver verifications
    """
    try:
        verifications = get_pending_driver_verifications()
        return simple_datetime_handler(verifications)
    except Exception as e:
        print(f"Error in get_pending_driver_verifications_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving pending driver verifications: {str(e)}")

# Driver Training Module endpoints
@router.post("/training-modules", response_model=DriverTrainingModuleResponse)
async def create_driver_training_module_endpoint(module: DriverTrainingModuleCreate):
    """
    Create a new driver training module
    """
    try:
        module_record = create_driver_training_module(
            module.title,
            module.description,
            module.duration_minutes,
            module.content_url,
            module.is_mandatory if module.is_mandatory is not None else True
        )
        
        if not module_record:
            raise HTTPException(status_code=500, detail="Error creating driver training module")
        
        return simple_datetime_handler(module_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_driver_training_module_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating driver training module: {str(e)}")

@router.get("/training-modules", response_model=list[DriverTrainingModuleResponse])
async def get_driver_training_modules_endpoint():
    """
    Get all driver training modules
    """
    try:
        modules = get_driver_training_modules()
        return simple_datetime_handler(modules)
    except Exception as e:
        print(f"Error in get_driver_training_modules_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver training modules: {str(e)}")

@router.get("/training-modules/{module_id}", response_model=DriverTrainingModuleResponse)
async def get_driver_training_module_endpoint(module_id: UUID):
    """
    Get a specific driver training module
    """
    try:
        module = get_driver_training_module(module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Driver training module not found")
        
        return simple_datetime_handler(module)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_driver_training_module_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver training module: {str(e)}")

@router.put("/training-modules/{module_id}", response_model=DriverTrainingModuleResponse)
async def update_driver_training_module_endpoint(module_id: UUID, module: DriverTrainingModuleUpdate):
    """
    Update a driver training module
    """
    try:
        module_record = update_driver_training_module(
            module_id,
            module.title,
            module.description,
            module.duration_minutes,
            module.content_url,
            module.is_mandatory
        )
        
        if not module_record:
            raise HTTPException(status_code=404, detail="Driver training module not found")
        
        return simple_datetime_handler(module_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_driver_training_module_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating driver training module: {str(e)}")

@router.delete("/training-modules/{module_id}")
async def delete_driver_training_module_endpoint(module_id: UUID):
    """
    Delete a driver training module
    """
    try:
        success = delete_driver_training_module(module_id)
        if not success:
            raise HTTPException(status_code=404, detail="Driver training module not found")
        
        return {"message": "Driver training module deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_driver_training_module_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error deleting driver training module: {str(e)}")

# Driver Training Completion endpoints
@router.post("/training-completions", response_model=DriverTrainingCompletionResponse)
async def create_driver_training_completion_endpoint(completion: DriverTrainingCompletionCreate):
    """
    Record a driver's completion of a training module
    """
    try:
        completion_record = create_driver_training_completion(
            completion.driver_id,
            completion.training_module_id,
            completion.score,
            completion.certificate_url
        )
        
        if not completion_record:
            raise HTTPException(status_code=500, detail="Error creating driver training completion")
        
        return simple_datetime_handler(completion_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_driver_training_completion_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating driver training completion: {str(e)}")

@router.get("/training-completions/{driver_id}", response_model=list[DriverTrainingCompletionResponse])
async def get_driver_training_completions_endpoint(driver_id: UUID):
    """
    Get all training completions for a driver
    """
    try:
        completions = get_driver_training_completions(driver_id)
        return simple_datetime_handler(completions)
    except Exception as e:
        print(f"Error in get_driver_training_completions_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver training completions: {str(e)}")

# Driver Incident endpoints
@router.post("/incidents", response_model=DriverIncidentResponse)
async def create_driver_incident_endpoint(incident: DriverIncidentCreate):
    """
    Create a new driver incident report
    """
    try:
        incident_record = create_driver_incident(
            incident.driver_id,
            incident.reporter_id,
            incident.incident_type,
            incident.description,
            incident.severity
        )
        
        if not incident_record:
            raise HTTPException(status_code=500, detail="Error creating driver incident")
        
        return simple_datetime_handler(incident_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_driver_incident_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating driver incident: {str(e)}")

@router.get("/incidents/{driver_id}", response_model=list[DriverIncidentResponse])
async def get_driver_incidents_endpoint(driver_id: UUID):
    """
    Get all incidents for a driver
    """
    try:
        incidents = get_driver_incidents(driver_id)
        return simple_datetime_handler(incidents)
    except Exception as e:
        print(f"Error in get_driver_incidents_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver incidents: {str(e)}")

@router.get("/incidents/pending", response_model=list[DriverIncidentResponse])
async def get_pending_driver_incidents_endpoint():
    """
    Get all pending driver incidents
    """
    try:
        incidents = get_pending_driver_incidents()
        return simple_datetime_handler(incidents)
    except Exception as e:
        print(f"Error in get_pending_driver_incidents_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving pending driver incidents: {str(e)}")

@router.put("/incidents/{incident_id}", response_model=DriverIncidentResponse)
async def update_driver_incident_endpoint(incident_id: UUID, incident: DriverIncidentUpdate):
    """
    Update a driver incident report
    """
    try:
        incident_record = update_driver_incident(
            incident_id,
            incident.status,
            incident.resolution_notes,
            incident.resolved_by
        )
        
        if not incident_record:
            raise HTTPException(status_code=404, detail="Driver incident not found")
        
        return simple_datetime_handler(incident_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_driver_incident_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating driver incident: {str(e)}")

# Driver Performance Metric endpoints
@router.post("/performance-metrics", response_model=DriverPerformanceMetricResponse)
async def create_driver_performance_metric_endpoint(metric: DriverPerformanceMetricCreate):
    """
    Create a new driver performance metric
    """
    try:
        metric_record = create_driver_performance_metric(
            metric.driver_id,
            metric.metric_type,
            metric.score,
            metric.period_start,
            metric.period_end,
            metric.notes
        )
        
        if not metric_record:
            raise HTTPException(status_code=500, detail="Error creating driver performance metric")
        
        return simple_datetime_handler(metric_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_driver_performance_metric_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating driver performance metric: {str(e)}")

@router.get("/performance-metrics/{driver_id}", response_model=list[DriverPerformanceMetricResponse])
async def get_driver_performance_metrics_endpoint(driver_id: UUID):
    """
    Get all performance metrics for a driver
    """
    try:
        metrics = get_driver_performance_metrics(driver_id)
        return simple_datetime_handler(metrics)
    except Exception as e:
        print(f"Error in get_driver_performance_metrics_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving driver performance metrics: {str(e)}")

@router.get("/performance-metrics/drivers/{min_score}/{max_score}", response_model=list[DriverPerformanceMetricResponse])
async def get_drivers_by_performance_score_endpoint(min_score: float, max_score: float):
    """
    Get drivers within a performance score range
    """
    try:
        drivers = get_drivers_by_performance_score(min_score, max_score)
        return simple_datetime_handler(drivers)
    except Exception as e:
        print(f"Error in get_drivers_by_performance_score_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving drivers by performance score: {str(e)}")