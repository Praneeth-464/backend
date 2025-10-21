#!/usr/bin/env python3
"""
Test script to verify JWT token creation and verification
"""

from datetime import timedelta
from app.utils.jwt_utils import create_access_token, verify_token
from app.schemas import TokenData

def test_jwt():
    """Test JWT token creation and verification"""
    
    # Test data
    test_data = {"sub": "test@example.com"}
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data=test_data, expires_delta=access_token_expires
    )
    
    print(f"Created access token: {access_token}")
    
    # Test token verification
    class MockCredentialsException(Exception):
        pass
    
    credentials_exception = MockCredentialsException("Could not validate credentials")
    
    try:
        token_data = verify_token(access_token, credentials_exception)
        print(f"Token verification successful: {token_data}")
        print(f"Email from token: {token_data.email}")
        print("SUCCESS: JWT authentication is working correctly")
    except Exception as e:
        print(f"Token verification failed: {e}")
        print("FAILURE: JWT authentication is not working correctly")

if __name__ == "__main__":
    test_jwt()