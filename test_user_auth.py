#!/usr/bin/env python3
"""
Test script to verify user creation and authentication with real database
"""

import os
import sys
from datetime import datetime
from app.schemas import UserCreate
from app.crud import create_user, get_user_by_email
from app.utils.jwt_utils import verify_password

def test_user_auth():
    """Test user creation and authentication"""
    
    # Test data
    user_data = UserCreate(
        name="Test User",
        email="test@example.com",
        password="securepassword123"
    )
    
    print("Testing user creation and authentication...")
    
    # Test user creation
    try:
        print("Creating user...")
        user = create_user(user_data)
        print(f"User created successfully: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")
        # If user already exists, that's okay for testing
        user = get_user_by_email(user_data.email)
        if user:
            print(f"User already exists: {user}")
        else:
            print("Failed to create or retrieve user")
            return
    
    # Test user retrieval
    print("\nRetrieving user by email...")
    retrieved_user = get_user_by_email(user_data.email)
    if retrieved_user:
        print(f"User retrieved successfully: {retrieved_user}")
        
        # Test password verification
        print("\nVerifying password...")
        user_dict = retrieved_user.dict()
        if verify_password(user_data.password, user_dict.get('password_hash', '')):
            print("Password verification successful!")
            print("SUCCESS: User authentication is working correctly")
        else:
            print("Password verification failed!")
            print("FAILURE: Password verification not working")
    else:
        print("Failed to retrieve user")
        print("FAILURE: User retrieval not working")

if __name__ == "__main__":
    test_user_auth()