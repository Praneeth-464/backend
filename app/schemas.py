from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, time
from uuid import UUID

if TYPE_CHECKING:
    from .schemas import DriverResponse

# Custom JSON encoder for datetime objects
class CustomBaseModel(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

# Authentication schemas
class UserCreate(CustomBaseModel):
    name: str
    email: str
    password: str

class UserLogin(CustomBaseModel):
    email: str
    password: str

class UserResponse(CustomBaseModel):
    id: UUID
    name: str
    email: str
    role: str
    email_verified: bool
    email_verification_token: Optional[str] = None
    email_verification_sent_at: Optional[datetime] = None
    created_at: datetime
    last_login: Optional[datetime] = None

class UserProfileUpdate(CustomBaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Token(CustomBaseModel):
    access_token: str
    token_type: str
    role: Optional[str] = None

class TokenData(CustomBaseModel):
    email: Optional[str] = None

# Verification schemas
class VerifyEmailRequest(CustomBaseModel):
    token: str

class ResendVerificationRequest(CustomBaseModel):
    email: str

# OTP schemas
class OTPRequest(CustomBaseModel):
    email: str

class OTPVerifyRequest(CustomBaseModel):
    email: str
    otp: str

class OTPLoginRequest(CustomBaseModel):
    email: str
    otp: str

# Rider schemas
class RiderCreate(CustomBaseModel):
    user_id: Optional[UUID] = None
    name: str
    email: str
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    preferred_departure: Optional[datetime] = None
    preferred_arrival: Optional[datetime] = None
    beta: Optional[float] = 0.5  # patience factor

class RideRequestCreate(RiderCreate):
    pass

class RiderResponse(RiderCreate):
    id: UUID
    status: str
    created_at: datetime

class RiderMatchResponse(RiderResponse):
    matched_driver: Optional['DriverResponse'] = None
    match_details: Optional[dict] = None

# Driver schemas
class DriverCreate(CustomBaseModel):
    user_id: Optional[UUID] = None
    name: str
    email: str
    current_lat: float
    current_lon: float
    available: Optional[bool] = True
    rating: Optional[float] = 5.0
    license_number: Optional[str] = None
    license_expiry_date: Optional[datetime] = None
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[int] = None
    vehicle_registration: Optional[str] = None
    vehicle_insurance_expiry: Optional[datetime] = None

class DriverUpdateLocation(CustomBaseModel):
    current_lat: float
    current_lon: float
    available: Optional[bool] = True

class DriverResponse(DriverCreate):
    id: UUID
    background_check_status: str = "pending"
    safety_training_completed: bool = False
    total_incidents: int = 0
    performance_score: float = 100.00

# Update the forward reference
RiderMatchResponse.model_rebuild()

# Driver Verification schemas
class DriverVerificationCreate(CustomBaseModel):
    driver_id: UUID
    verification_type: str  # 'background_check', 'vehicle_inspection', 'safety_training'
    document_url: Optional[str] = None
    notes: Optional[str] = None
    verified_by: Optional[UUID] = None

class DriverVerificationUpdate(CustomBaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None

class DriverVerificationResponse(DriverVerificationCreate):
    id: UUID
    status: str = "pending"
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# Driver Training Module schemas
class DriverTrainingModuleCreate(CustomBaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    content_url: Optional[str] = None
    is_mandatory: Optional[bool] = True

class DriverTrainingModuleUpdate(CustomBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    content_url: Optional[str] = None
    is_mandatory: Optional[bool] = None

class DriverTrainingModuleResponse(DriverTrainingModuleCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

# Driver Training Completion schemas
class DriverTrainingCompletionCreate(CustomBaseModel):
    driver_id: UUID
    training_module_id: UUID
    score: Optional[float] = None
    certificate_url: Optional[str] = None

class DriverTrainingCompletionResponse(DriverTrainingCompletionCreate):
    id: UUID
    completed_at: datetime
    created_at: datetime

# Driver Incident schemas
class DriverIncidentCreate(CustomBaseModel):
    driver_id: UUID
    reporter_id: UUID
    incident_type: str  # 'accident', 'complaint', 'violation'
    description: str
    severity: str  # 'low', 'medium', 'high', 'critical'

class DriverIncidentUpdate(CustomBaseModel):
    status: Optional[str] = None
    resolution_notes: Optional[str] = None
    resolved_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None

class DriverIncidentResponse(DriverIncidentCreate):
    id: UUID
    status: str = "reported"
    resolution_notes: Optional[str] = None
    resolved_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# Driver Performance Metric schemas
class DriverPerformanceMetricCreate(CustomBaseModel):
    driver_id: UUID
    metric_type: str  # 'punctuality', 'safety', 'customer_service', 'vehicle_maintenance'
    score: float
    period_start: datetime
    period_end: datetime
    notes: Optional[str] = None

class DriverPerformanceMetricResponse(DriverPerformanceMetricCreate):
    id: UUID
    created_at: datetime

# Ride schemas
class RideCreate(CustomBaseModel):
    user_id: Optional[UUID] = None
    rider_id: Optional[UUID] = None
    driver_id: Optional[UUID] = None
    algorithm: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    fare: Optional[float] = None
    utility: Optional[float] = None
    status: Optional[str] = "requested"

class RideResponse(RideCreate):
    id: UUID

# Matching schemas
class MatchRequest(CustomBaseModel):
    algorithm: str  # "RGA", "RGA++", or "IV"

class Assignment(CustomBaseModel):
    rider_id: UUID
    driver_id: UUID
    utility: float

class MatchResponse(CustomBaseModel):
    algorithm: str
    assignments: List[Assignment]
    metrics: dict

# Metrics schemas
class MetricsResponse(CustomBaseModel):
    gini: float
    social_welfare: float
    timestamp: datetime

# Notification schemas
class NotificationCreate(CustomBaseModel):
    user_id: UUID
    title: str
    message: str
    type: str

class NotificationResponse(CustomBaseModel):
    id: UUID
    user_id: UUID
    title: str
    message: str
    type: str
    read: bool
    created_at: datetime

# Rating schemas
class RatingCreate(CustomBaseModel):
    user_id: Optional[UUID] = None
    rating: int  # 1-5 stars
    review: Optional[str] = None
    tip: Optional[float] = None

class RatingResponse(CustomBaseModel):
    id: UUID
    user_id: UUID
    ride_id: UUID
    rider_id: UUID
    driver_id: UUID
    rating: int
    review: Optional[str] = None
    tip: Optional[float] = None
    created_at: datetime

class DriverRatingsResponse(CustomBaseModel):
    driver_id: UUID
    average_rating: float
    total_ratings: int
    reviews: List[RatingResponse]

# Ride Group schemas for shared rides
class RideGroupCreate(CustomBaseModel):
    name: str
    creator_id: UUID
    estimated_fare: Optional[float] = None

class RideGroupUpdate(CustomBaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    final_fare: Optional[float] = None

class RideGroupResponse(RideGroupCreate):
    id: UUID
    status: str = "pending"
    final_fare: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class RideGroupMemberCreate(CustomBaseModel):
    ride_group_id: UUID
    user_id: UUID
    role: Optional[str] = "member"
    fare_share_percentage: Optional[float] = 0

class RideGroupMemberUpdate(CustomBaseModel):
    status: Optional[str] = None
    fare_share_percentage: Optional[float] = None
    accepted_at: Optional[datetime] = None

class RideGroupMemberResponse(RideGroupMemberCreate):
    id: UUID
    role: Optional[str] = "member"
    status: str = "invited"
    invited_at: datetime
    accepted_at: Optional[datetime] = None
    created_at: datetime

# Subscription Plan schemas
class SubscriptionPlanCreate(CustomBaseModel):
    name: str
    description: Optional[str] = None
    price: float
    billing_cycle: str  # 'monthly', 'annual'
    ride_limit: Optional[int] = None
    priority_booking: Optional[bool] = False
    discount_percentage: Optional[float] = 0.00
    cancellation_fee_waiver: Optional[bool] = False
    customer_support_priority: Optional[str] = "standard"  # 'standard', 'priority', 'dedicated'

class SubscriptionPlanUpdate(CustomBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    billing_cycle: Optional[str] = None
    ride_limit: Optional[int] = None
    priority_booking: Optional[bool] = None
    discount_percentage: Optional[float] = None
    cancellation_fee_waiver: Optional[bool] = None
    customer_support_priority: Optional[str] = None

class SubscriptionPlanResponse(SubscriptionPlanCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

# User Subscription schemas
class UserSubscriptionCreate(CustomBaseModel):
    user_id: UUID
    plan_id: UUID
    start_date: datetime
    end_date: Optional[datetime] = None
    auto_renew: Optional[bool] = True
    payment_method_id: Optional[str] = None

class UserSubscriptionUpdate(CustomBaseModel):
    status: Optional[str] = None
    end_date: Optional[datetime] = None
    auto_renew: Optional[bool] = None
    payment_method_id: Optional[str] = None

class UserSubscriptionResponse(UserSubscriptionCreate):
    id: UUID
    status: str = "active"
    created_at: datetime
    updated_at: datetime

# Recurring Ride schemas
class RecurringRideCreate(CustomBaseModel):
    user_id: UUID
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    frequency: str  # 'daily', 'weekly', 'monthly'
    days_of_week: Optional[List[int]] = None  # Array of days (0=Sunday, 1=Monday, etc.) for weekly
    day_of_month: Optional[int] = None  # Day of month for monthly (1-31)
    start_time: time  # Time of day for the ride
    end_date: Optional[datetime] = None  # When to stop creating rides (NULL for indefinite)
    preferences: Optional[dict] = None  # Ride preferences

class RecurringRideUpdate(CustomBaseModel):
    frequency: Optional[str] = None
    days_of_week: Optional[List[int]] = None
    day_of_month: Optional[int] = None
    start_time: Optional[time] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    preferences: Optional[dict] = None

class RecurringRideResponse(RecurringRideCreate):
    id: UUID
    status: str = "active"
    created_at: datetime
    updated_at: datetime

# Generated Scheduled Ride schemas
class GeneratedScheduledRideCreate(CustomBaseModel):
    recurring_ride_id: UUID
    scheduled_ride_id: UUID

class GeneratedScheduledRideResponse(GeneratedScheduledRideCreate):
    id: UUID
    generation_date: datetime

# Enhanced schemas for additional functionalities
class FareEstimateRequest(CustomBaseModel):
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    rider_beta: Optional[float] = 0.5
    traffic_multiplier: Optional[float] = 1.0

class FareEstimateResponse(CustomBaseModel):
    estimated_fare: float
    distance_km: float
    estimated_duration_minutes: float
    base_fare: float
    distance_fare: float
    time_fare: float
    surge_multiplier: Optional[float] = 1.0

# Algorithm-based fare estimation schemas
class AlgorithmFareEstimateRequest(CustomBaseModel):
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    rider_beta: Optional[float] = 0.5
    traffic_multiplier: Optional[float] = 1.0
    algorithm: str  # "RGA", "RGA++", or "IV"

class AlgorithmFareEstimateResponse(CustomBaseModel):
    algorithm: str
    estimated_fare: float
    distance_km: float
    estimated_duration_minutes: float
    base_fare: float
    distance_fare: float
    time_fare: float
    surge_multiplier: Optional[float] = 1.0
    utility: Optional[float] = None
    metrics: Optional[dict] = None

class RidePreference(CustomBaseModel):
    min_driver_rating: Optional[float] = None
    ride_type: Optional[str] = None  # "solo", "shared", "premium"
    accessibility_needs: Optional[List[str]] = None  # "wheelchair", "pet", etc.

class DriverPreference(CustomBaseModel):
    no_heavy_luggage: Optional[bool] = None
    no_pets: Optional[bool] = None
    preferred_areas: Optional[List[str]] = None

class SOSRequest(CustomBaseModel):
    ride_id: UUID
    message: Optional[str] = "Emergency SOS"

class SOSResponse(CustomBaseModel):
    message: str
    emergency_contact_notified: bool
    location_shared: bool

class WalletTransactionCreate(CustomBaseModel):
    user_id: Optional[UUID] = None
    amount: float
    transaction_type: str  # "credit", "debit"
    description: str

class WalletTransaction(WalletTransactionCreate):
    balance_after: float
    created_at: datetime
    id: UUID

class ScheduledRideRequest(CustomBaseModel):
    user_id: Optional[UUID] = None
    rider_id: UUID
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    scheduled_time: datetime
    preferences: Optional[RidePreference] = None

class ScheduledRideResponse(CustomBaseModel):
    id: UUID
    user_id: UUID
    rider_id: UUID
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    scheduled_time: datetime
    status: str  # "scheduled", "confirmed", "completed", "cancelled"
    created_at: datetime

class LoyaltyPoints(CustomBaseModel):
    user_id: UUID
    points: int
    level: str  # "bronze", "silver", "gold", "platinum"
    next_level_points: int

class AnalyticsRequest(CustomBaseModel):
    user_id: UUID
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: List[str]  # "spending", "rides", "ratings", etc.

class AnalyticsResponse(CustomBaseModel):
    user_id: UUID
    total_rides: int
    total_spent: float
    average_rating: float
    favorite_destinations: List[dict]
    spending_patterns: dict
    ride_history: List[dict]

# Schedule schemas
class ScheduleCreate(CustomBaseModel):
    user_id: Optional[UUID] = None
    algorithm: str
    metadata: Optional[dict] = None

class ScheduleResponse(CustomBaseModel):
    id: UUID
    user_id: UUID
    algorithm: str
    metadata: Optional[dict] = None
    created_at: datetime

# Emergency contact schemas
class EmergencyContactCreate(CustomBaseModel):
    name: str
    phone: str
    relationship: Optional[str] = None
    is_primary: Optional[bool] = False

class EmergencyContactResponse(EmergencyContactCreate):
    id: UUID
    user_id: UUID
    created_at: datetime

# Referral schemas
class ReferralCreate(CustomBaseModel):
    referee_email: str

class ReferralResponse(CustomBaseModel):
    id: UUID
    referrer_id: UUID
    referee_id: Optional[UUID] = None
    referral_code: str
    status: str
    reward_points: int
    created_at: datetime
    completed_at: Optional[datetime] = None

# Chat message schemas
class ChatMessageCreate(CustomBaseModel):
    ride_id: UUID
    message: str

class ChatMessageResponse(ChatMessageCreate):
    id: UUID
    sender_id: UUID
    sender_type: str
    is_read: bool
    created_at: datetime

# Emergency SOS schemas
class EmergencySOSRequest(CustomBaseModel):
    ride_id: UUID
    message: Optional[str] = "Emergency SOS"

class EmergencySOSResponse(CustomBaseModel):
    message: str
    emergency_contact_notified: bool
    location_shared: bool

# Analytics schemas
class SystemMetrics(CustomBaseModel):
    total_rides: int
    active_riders: int
    active_drivers: int
    average_rating: float
    timestamp: datetime

class AlgorithmPerformance(CustomBaseModel):
    name: str
    gini_index: float
    social_welfare: float
    execution_time: float
    usage_count: int

class UserAnalytics(CustomBaseModel):
    user_id: UUID
    total_rides: int
    total_spent: float
    favorite_destinations: List[dict]
    preferred_time: str
    timestamp: datetime

class DriverEarnings(CustomBaseModel):
    driver_id: UUID
    total_earnings: float
    total_rides: int
    average_rating: float
    hours_online: float
    timestamp: datetime

# Tracking schemas
class DriverLocationUpdate(CustomBaseModel):
    user_id: Optional[UUID] = None
    lat: float
    lon: float
    speed: Optional[float] = 0.0
    heading: Optional[float] = 0.0

class RideTracking(CustomBaseModel):
    user_id: UUID
    ride_id: UUID
    driver_location: dict
    estimated_arrival: datetime
    distance_to_pickup: float
    eta_dropoff: datetime


class EstimatedFareResponse(CustomBaseModel):
    ride_id: UUID
    algorithm: str
    status: str
    estimated_fare: float
    distance_km: float
    estimated_duration_minutes: float
    base_fare: float
    distance_fare: float
    time_fare: float
    surge_multiplier: float
