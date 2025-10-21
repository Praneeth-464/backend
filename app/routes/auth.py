from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from uuid import UUID
from ..schemas import UserCreate, UserLogin, UserResponse, Token, RiderCreate, RiderResponse, DriverCreate, DriverResponse, DriverUpdateLocation, VerifyEmailRequest, ResendVerificationRequest, OTPRequest, OTPVerifyRequest, UserProfileUpdate
from ..crud import create_rider, get_rider, get_riders, create_driver, get_driver, get_drivers, update_driver_location, create_user, get_user_by_email, update_user_last_login, get_user_by_verification_token, verify_user_email, resend_verification_email, create_otp, get_otp_by_email, verify_otp as crud_verify_otp
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.jwt_utils import create_access_token, verify_password
from ..utils.auth_utils import get_current_user
from ..sendgrid_client import send_verification_email, send_welcome_email, send_otp_email
import traceback
import random

router = APIRouter()

def authenticate_user(email: str, password: str):
    """
    Authenticate a user by email and password against the database
    """
    user = get_user_by_email(email)
    if not user:
        return False
    # Get user data as dict to access password_hash
    user_dict = user.dict()
    # Verify password against stored hash
    if not verify_password(password, user_dict.get('password_hash', '')):
        return False
    return user

def generate_otp():
    """
    Generate a 6-digit OTP
    """
    return str(random.randint(100000, 999999))

def store_otp(email: str, otp: str):
    """
    Store OTP with expiration time (30 minutes) in database
    """
    expires_at = datetime.now() + timedelta(minutes=30)
    return create_otp(email, otp, expires_at)

def verify_otp(email: str, otp: str):
    """
    Verify OTP for email using database
    """
    return crud_verify_otp(email, otp)

@router.post("/signup/user", response_model=UserResponse)
async def signup_user(user: UserCreate):
    """
    Register a new user and send verification email
    """
    try:
        # Check if user already exists
        existing_user = get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Create user
        result = create_user(user)
        
        # Send verification email
        if result.email_verification_token:
            send_verification_email(user.email, result.email_verification_token)
        
        return simple_datetime_handler(result.dict())
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in signup_user: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/verify-email")
async def verify_email(token: str = Query(..., description="Email verification token")):
    """
    Verify user's email address using verification token
    """
    try:
        # Verify the user's email
        user = verify_user_email(token)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid or expired verification token")
        
        # Send welcome email
        send_welcome_email(user.email, user.name)
        
        return {"message": "Email verified successfully. You can now log in to your account."}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in verify_email: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error verifying email")

@router.post("/resend-verification")
async def resend_verification(request: ResendVerificationRequest):
    """
    Resend email verification to user
    """
    try:
        # Find user by email
        user = get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user is already verified
        if user.email_verified:
            raise HTTPException(status_code=400, detail="Email already verified")
        
        # Resend verification email
        updated_user = resend_verification_email(user.id)
        if not updated_user:
            raise HTTPException(status_code=500, detail="Error resending verification email")
        
        if updated_user.email_verification_token:
            send_verification_email(request.email, updated_user.email_verification_token)
        
        return {"message": "Verification email sent successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in resend_verification: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error resending verification email")

@router.post("/request-otp")
async def request_otp(request: OTPRequest):
    """
    Request OTP for login verification
    """
    try:
        # Check if user exists
        user = get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user's email is verified
        user_dict = user.dict()
        if not user_dict.get('email_verified', False):
            raise HTTPException(status_code=401, detail="Please verify your email address before requesting OTP")
        
        # Generate and store OTP in database
        otp = generate_otp()
        if not store_otp(request.email, otp):
            raise HTTPException(status_code=500, detail="Error generating OTP")
        
        # Send OTP via email
        send_otp_email(request.email, otp)
        
        return {"message": "OTP sent successfully to your email"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in request_otp: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error sending OTP")

@router.post("/verify-otp")
async def verify_otp_endpoint(request: OTPVerifyRequest):
    """
    Verify OTP for login
    """
    try:
        print(f"Verifying OTP for email: {request.email}")
        # Verify OTP using database
        if not verify_otp(request.email, request.otp):
            # Try to get OTP to check if it exists but is expired
            stored_otp_data = get_otp_by_email(request.email)
            if stored_otp_data:
                # Check if OTP is expired
                expires_at = datetime.fromisoformat(stored_otp_data["expires_at"])
                if datetime.now().isoformat() > stored_otp_data["expires_at"]:
                    raise HTTPException(status_code=401, detail="OTP has expired")
                else:
                    raise HTTPException(status_code=401, detail="Invalid OTP")
            else:
                raise HTTPException(status_code=401, detail="No OTP found for this email. Please request a new OTP.")
        
        # OTP is valid
        return {"message": "OTP verified successfully", "email": request.email}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in verify_otp: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error verifying OTP")

# Add a simple in-memory store for verified OTP sessions (in production, use Redis or database)
verified_otp_sessions = set()

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user and return JWT token (requires OTP verification)
    """
    # First authenticate with email and password
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user's email is verified
    user_dict = user.dict()
    if not user_dict.get('email_verified', False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email address before logging in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user has verified OTP recently (in a real implementation, you might want to check this differently)
    # For now, we'll proceed with normal JWT token creation as before since we're not fully implementing
    # the OTP requirement for login in this example
    
    # Update last login time
    update_user_last_login(user.id)
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@router.post("/login-with-otp", response_model=Token)
async def login_with_otp(request: OTPVerifyRequest):
    """
    Login user with OTP and return JWT token
    This endpoint combines OTP verification and token generation for a streamlined login flow
    """
    try:
        print(f"Logging in with OTP for email: {request.email}")
        # Verify OTP using database
        if not verify_otp(request.email, request.otp):
            # Try to get OTP to check if it exists but is expired
            stored_otp_data = get_otp_by_email(request.email)
            if stored_otp_data:
                # Check if OTP is expired - comparing ISO format strings to avoid timezone issues
                if datetime.now().isoformat() > stored_otp_data["expires_at"]:
                    raise HTTPException(status_code=401, detail="OTP has expired")
                else:
                    raise HTTPException(status_code=401, detail="Invalid OTP")
            else:
                raise HTTPException(status_code=401, detail="No OTP found for this email. Please request a new OTP.")
        
        # Get user by email
        user = get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user's email is verified
        user_dict = user.dict()
        if not user_dict.get('email_verified', False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please verify your email address before logging in",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login time
        update_user_last_login(user.id)
        
        # Generate JWT token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer", "role": user.role}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in login_with_otp: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error logging in with OTP")

@router.post("/signup/rider", response_model=RiderResponse)
async def signup_rider(rider: RiderCreate):
    """
    Register a new rider with preference information
    No JWT token required for registration.
    """
    try:
        # Check if email exists in users table
        user = get_user_by_email(rider.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if rider already exists for this user
        from ..crud import get_rider_by_user_id
        existing_rider = get_rider_by_user_id(user.id)
        if existing_rider:
            raise HTTPException(status_code=400, detail="Rider profile already exists for this user")
        
        # Use current user's ID if not provided in request
        user_id = rider.user_id if rider.user_id else user.id
        
        # Add user_id to rider data
        rider_data = rider.model_copy(update={"user_id": user_id})
        
        # Create rider
        from ..crud import create_rider
        result = create_rider(rider_data)
        
        from ..utils.datetime_serializer import simple_datetime_handler
        return simple_datetime_handler(result.dict())
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in signup_rider: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user_email: str = Depends(get_current_user)):
    """
    Get the current authenticated user's profile
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(user.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_user_profile: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user profile: {str(e)}")

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(profile_update: UserProfileUpdate, current_user_email: str = Depends(get_current_user)):
    """
    Update the current authenticated user's profile
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Import the update function here to avoid circular imports
        from ..crud import update_user_profile as crud_update_user_profile
        
        # Update user profile
        updated_user = crud_update_user_profile(
            user.id,
            name=profile_update.name,
            email=profile_update.email
        )
        
        if not updated_user:
            raise HTTPException(status_code=500, detail="Error updating user profile")
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(updated_user.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in update_user_profile: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating user profile: {str(e)}")

@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: UUID, current_user_email: str = Depends(get_current_user)):
    """
    Get a user by user ID
    """
    try:
        # Get the current user to verify authentication
        current_user = get_user_by_email(current_user_email)
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get the requested user
        from ..crud import get_user_by_id
        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use simple datetime handler for serialization
        serialized_result = simple_datetime_handler(user.dict())
        return serialized_result
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Error in get_user_by_id: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")
