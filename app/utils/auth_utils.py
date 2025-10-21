from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .jwt_utils import verify_token

# OAuth2 scheme for JWT tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# In-memory store for active sessions (in production, use Redis or database)
# For development, we'll make this optional to avoid issues with server restarts
active_sessions = set()

# Dependency for getting current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify the JWT token - this is the primary authentication check
    try:
        email = verify_token(token, credentials_exception)
        return email
    except Exception as e:
        raise credentials_exception