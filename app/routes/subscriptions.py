from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from datetime import datetime, time
from ..schemas import (
    SubscriptionPlanCreate, SubscriptionPlanUpdate, SubscriptionPlanResponse,
    UserSubscriptionCreate, UserSubscriptionUpdate, UserSubscriptionResponse,
    RecurringRideCreate, RecurringRideUpdate, RecurringRideResponse,
    GeneratedScheduledRideCreate, GeneratedScheduledRideResponse
)
from ..crud import (
    create_subscription_plan, get_subscription_plans, get_subscription_plan, update_subscription_plan, delete_subscription_plan,
    create_user_subscription, get_user_subscriptions, get_user_active_subscription, get_subscription, update_user_subscription, cancel_user_subscription,
    create_recurring_ride, get_user_recurring_rides, get_recurring_ride, update_recurring_ride, pause_recurring_ride, resume_recurring_ride, cancel_recurring_ride, get_active_recurring_rides,
    create_generated_scheduled_ride, get_generated_scheduled_rides,
    get_user_by_email
)
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

# Subscription Plan endpoints (admin endpoints - no authentication required)
@router.post("/plans", response_model=SubscriptionPlanResponse)
async def create_subscription_plan_endpoint(plan: SubscriptionPlanCreate):
    """
    Create a new subscription plan
    """
    try:
        plan_record = create_subscription_plan(
            plan.name,
            plan.description,
            plan.price,
            plan.billing_cycle,
            plan.ride_limit,
            plan.priority_booking if plan.priority_booking is not None else False,
            plan.discount_percentage if plan.discount_percentage is not None else 0.00,
            plan.cancellation_fee_waiver if plan.cancellation_fee_waiver is not None else False,
            plan.customer_support_priority if plan.customer_support_priority is not None else "standard"
        )
        
        if not plan_record:
            raise HTTPException(status_code=500, detail="Error creating subscription plan")
        
        return simple_datetime_handler(plan_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_subscription_plan_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating subscription plan: {str(e)}")

@router.get("/plans", response_model=list[SubscriptionPlanResponse])
async def get_subscription_plans_endpoint():
    """
    Get all subscription plans
    """
    try:
        plans = get_subscription_plans()
        return simple_datetime_handler(plans)
    except Exception as e:
        print(f"Error in get_subscription_plans_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving subscription plans: {str(e)}")

@router.get("/plans/{plan_id}", response_model=SubscriptionPlanResponse)
async def get_subscription_plan_endpoint(plan_id: UUID):
    """
    Get a subscription plan by ID
    """
    try:
        plan = get_subscription_plan(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Subscription plan not found")
        
        return simple_datetime_handler(plan)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_subscription_plan_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving subscription plan: {str(e)}")

@router.put("/plans/{plan_id}", response_model=SubscriptionPlanResponse)
async def update_subscription_plan_endpoint(plan_id: UUID, plan: SubscriptionPlanUpdate):
    """
    Update a subscription plan
    """
    try:
        plan_record = update_subscription_plan(
            plan_id,
            plan.name,
            plan.description,
            plan.price,
            plan.billing_cycle,
            plan.ride_limit,
            plan.priority_booking,
            plan.discount_percentage,
            plan.cancellation_fee_waiver,
            plan.customer_support_priority
        )
        
        if not plan_record:
            raise HTTPException(status_code=404, detail="Subscription plan not found")
        
        return simple_datetime_handler(plan_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_subscription_plan_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating subscription plan: {str(e)}")

@router.delete("/plans/{plan_id}")
async def delete_subscription_plan_endpoint(plan_id: UUID):
    """
    Delete a subscription plan
    """
    try:
        success = delete_subscription_plan(plan_id)
        if not success:
            raise HTTPException(status_code=404, detail="Subscription plan not found")
        
        return {"message": "Subscription plan deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_subscription_plan_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error deleting subscription plan: {str(e)}")

# User Subscription endpoints
@router.post("/", response_model=UserSubscriptionResponse)
async def create_user_subscription_endpoint(subscription: UserSubscriptionCreate, current_user_email: str = Depends(get_current_user)):
    """
    Create a new user subscription
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use authenticated user's ID
        user_id = subscription.user_id if subscription.user_id else user.id
        
        subscription_record = create_user_subscription(
            user_id,
            subscription.plan_id,
            subscription.start_date,
            subscription.end_date,
            subscription.auto_renew if subscription.auto_renew is not None else True,
            subscription.payment_method_id
        )
        
        if not subscription_record:
            raise HTTPException(status_code=500, detail="Error creating user subscription")
        
        return simple_datetime_handler(subscription_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_user_subscription_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating user subscription: {str(e)}")

@router.get("/user", response_model=list[UserSubscriptionResponse])
async def get_user_subscriptions_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Get all subscriptions for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        subscriptions = get_user_subscriptions(user.id)
        return simple_datetime_handler(subscriptions)
    except Exception as e:
        print(f"Error in get_user_subscriptions_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user subscriptions: {str(e)}")

@router.get("/user/active", response_model=UserSubscriptionResponse)
async def get_user_active_subscription_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Get the active subscription for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        subscription = get_user_active_subscription(user.id)
        if not subscription:
            raise HTTPException(status_code=404, detail="Active subscription not found")
        
        return simple_datetime_handler(subscription)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_user_active_subscription_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user active subscription: {str(e)}")

@router.get("/{subscription_id}", response_model=UserSubscriptionResponse)
async def get_subscription_endpoint(subscription_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Get a subscription by ID
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        subscription = get_subscription(subscription_id)
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        # Verify user owns this subscription
        if str(subscription.get("user_id")) != str(user.id):
            raise HTTPException(status_code=403, detail="Not authorized to access this subscription")
        
        return simple_datetime_handler(subscription)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_subscription_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving subscription: {str(e)}")

@router.put("/{subscription_id}", response_model=UserSubscriptionResponse)
async def update_user_subscription_endpoint(subscription_id: UUID, subscription: UserSubscriptionUpdate, current_user_email: str = Depends(get_current_user)):
    """
    Update a user subscription
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify user owns this subscription
        existing_subscription = get_subscription(subscription_id)
        if not existing_subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        if str(existing_subscription.get("user_id")) != str(user.id):
            raise HTTPException(status_code=403, detail="Not authorized to update this subscription")
        
        subscription_record = update_user_subscription(
            subscription_id,
            subscription.status,
            subscription.end_date,
            subscription.auto_renew,
            subscription.payment_method_id
        )
        
        if not subscription_record:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        return simple_datetime_handler(subscription_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_user_subscription_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating user subscription: {str(e)}")

@router.post("/{subscription_id}/cancel", response_model=UserSubscriptionResponse)
async def cancel_user_subscription_endpoint(subscription_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Cancel a user subscription
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify user owns this subscription
        existing_subscription = get_subscription(subscription_id)
        if not existing_subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        if str(existing_subscription.get("user_id")) != str(user.id):
            raise HTTPException(status_code=403, detail="Not authorized to cancel this subscription")
        
        subscription_record = cancel_user_subscription(subscription_id)
        if not subscription_record:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        return simple_datetime_handler(subscription_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in cancel_user_subscription_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error canceling user subscription: {str(e)}")

# Recurring Ride endpoints
@router.post("/recurring", response_model=RecurringRideResponse)
async def create_recurring_ride_endpoint(ride: RecurringRideCreate):
    """
    Create a new recurring ride
    """
    try:
        ride_record = create_recurring_ride(
            ride.user_id,
            ride.origin_lat,
            ride.origin_lon,
            ride.destination_lat,
            ride.destination_lon,
            ride.frequency,
            ride.start_time.isoformat(),
            ride.end_date,
            ride.days_of_week,
            ride.day_of_month,
            ride.preferences
        )
        
        if not ride_record:
            raise HTTPException(status_code=500, detail="Error creating recurring ride")
        
        return simple_datetime_handler(ride_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_recurring_ride_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating recurring ride: {str(e)}")

@router.get("/recurring/user/{user_id}", response_model=list[RecurringRideResponse])
async def get_user_recurring_rides_endpoint(user_id: UUID):
    """
    Get all recurring rides for a user
    """
    try:
        rides = get_user_recurring_rides(user_id)
        return simple_datetime_handler(rides)
    except Exception as e:
        print(f"Error in get_user_recurring_rides_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user recurring rides: {str(e)}")

@router.get("/recurring/{ride_id}", response_model=RecurringRideResponse)
async def get_recurring_ride_endpoint(ride_id: UUID):
    """
    Get a recurring ride by ID
    """
    try:
        ride = get_recurring_ride(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Recurring ride not found")
        
        return simple_datetime_handler(ride)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_recurring_ride_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving recurring ride: {str(e)}")

@router.put("/recurring/{ride_id}", response_model=RecurringRideResponse)
async def update_recurring_ride_endpoint(ride_id: UUID, ride: RecurringRideUpdate):
    """
    Update a recurring ride
    """
    try:
        start_time = ride.start_time.isoformat() if ride.start_time else None
        
        ride_record = update_recurring_ride(
            ride_id,
            ride.frequency,
            ride.days_of_week,
            ride.day_of_month,
            start_time,
            ride.end_date,
            ride.status,
            ride.preferences
        )
        
        if not ride_record:
            raise HTTPException(status_code=404, detail="Recurring ride not found")
        
        return simple_datetime_handler(ride_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_recurring_ride_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating recurring ride: {str(e)}")

@router.post("/recurring/{ride_id}/pause", response_model=RecurringRideResponse)
async def pause_recurring_ride_endpoint(ride_id: UUID):
    """
    Pause a recurring ride
    """
    try:
        ride_record = pause_recurring_ride(ride_id)
        if not ride_record:
            raise HTTPException(status_code=404, detail="Recurring ride not found")
        
        return simple_datetime_handler(ride_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in pause_recurring_ride_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error pausing recurring ride: {str(e)}")

@router.post("/recurring/{ride_id}/resume", response_model=RecurringRideResponse)
async def resume_recurring_ride_endpoint(ride_id: UUID):
    """
    Resume a paused recurring ride
    """
    try:
        ride_record = resume_recurring_ride(ride_id)
        if not ride_record:
            raise HTTPException(status_code=404, detail="Recurring ride not found")
        
        return simple_datetime_handler(ride_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in resume_recurring_ride_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error resuming recurring ride: {str(e)}")

@router.post("/recurring/{ride_id}/cancel", response_model=RecurringRideResponse)
async def cancel_recurring_ride_endpoint(ride_id: UUID):
    """
    Cancel a recurring ride
    """
    try:
        ride_record = cancel_recurring_ride(ride_id)
        if not ride_record:
            raise HTTPException(status_code=404, detail="Recurring ride not found")
        
        return simple_datetime_handler(ride_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in cancel_recurring_ride_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error cancelling recurring ride: {str(e)}")

@router.get("/recurring/active", response_model=list[RecurringRideResponse])
async def get_active_recurring_rides_endpoint():
    """
    Get all active recurring rides
    """
    try:
        rides = get_active_recurring_rides()
        return simple_datetime_handler(rides)
    except Exception as e:
        print(f"Error in get_active_recurring_rides_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving active recurring rides: {str(e)}")

# Generated Scheduled Ride endpoints
@router.post("/generated", response_model=GeneratedScheduledRideResponse)
async def create_generated_scheduled_ride_endpoint(ride: GeneratedScheduledRideCreate):
    """
    Create a record of a scheduled ride generated from a recurring ride
    """
    try:
        ride_record = create_generated_scheduled_ride(
            ride.recurring_ride_id,
            ride.scheduled_ride_id
        )
        
        if not ride_record:
            raise HTTPException(status_code=500, detail="Error creating generated scheduled ride")
        
        return simple_datetime_handler(ride_record)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_generated_scheduled_ride_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating generated scheduled ride: {str(e)}")

@router.get("/generated/{recurring_ride_id}", response_model=list[GeneratedScheduledRideResponse])
async def get_generated_scheduled_rides_endpoint(recurring_ride_id: UUID):
    """
    Get all scheduled rides generated from a recurring ride
    """
    try:
        rides = get_generated_scheduled_rides(recurring_ride_id)
        return simple_datetime_handler(rides)
    except Exception as e:
        print(f"Error in get_generated_scheduled_rides_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving generated scheduled rides: {str(e)}")