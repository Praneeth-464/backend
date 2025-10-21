from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Simple password comparison (removes hashing for testing only)
def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Compare plain password with stored password (no hashing)
    WARNING: This is insecure and should only be used for testing
    """
    return plain_password == stored_password

def get_password_hash(password: str) -> str:
    """
    Return password as-is (no hashing)
    WARNING: This is insecure and should only be used for testing
    """
    return password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    # Ensure SECRET_KEY is not None
    secret_key = SECRET_KEY or "default_secret_key_for_development_only"
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception) -> str:
    """
    Verify a JWT token and return email
    """
    try:
        # Ensure SECRET_KEY is not None
        secret_key = SECRET_KEY or "default_secret_key_for_development_only"
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception