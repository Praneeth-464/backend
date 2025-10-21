import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_database_otp():
    """
    Test the database-based OTP functionality
    """
    print("Testing database-based OTP functionality...")
    
    # Test user data (use an existing verified user)
    user_email = input("Enter your email: ")
    
    # 1. Request OTP
    print(f"\n[{datetime.now()}] Requesting OTP for {user_email}...")
    otp_request_data = {
        "email": user_email
    }
    try:
        otp_response = requests.post(f"{BASE_URL}/auth/request-otp", json=otp_request_data)
        print(f"OTP Request Status Code: {otp_response.status_code}")
        print(f"OTP Request Response: {otp_response.json()}")
        
        if otp_response.status_code != 200:
            print("OTP request failed. Exiting test.")
            return
    except Exception as e:
        print(f"Error requesting OTP: {e}")
        return
    
    # 2. Get OTP from user
    otp_code = input("Enter the OTP you received via email: ")
    
    # 3. Verify OTP
    print(f"\n[{datetime.now()}] Verifying OTP...")
    otp_verify_data = {
        "email": user_email,
        "otp": otp_code
    }
    try:
        verify_response = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_verify_data)
        print(f"OTP Verify Status Code: {verify_response.status_code}")
        print(f"OTP Verify Response: {verify_response.json()}")
        
        if verify_response.status_code == 200:
            print("OTP verification successful!")
        else:
            print("OTP verification failed.")
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return
    
    # 4. Try to verify the same OTP again (should fail)
    print(f"\n[{datetime.now()}] Testing OTP reuse (should fail)...")
    try:
        verify_response2 = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_verify_data)
        print(f"OTP Reuse Status Code: {verify_response2.status_code}")
        print(f"OTP Reuse Response: {verify_response2.json()}")
        
        if verify_response2.status_code == 401:
            print("OTP reuse correctly prevented!")
        else:
            print("OTP reuse prevention failed.")
    except Exception as e:
        print(f"Error testing OTP reuse: {e}")

if __name__ == "__main__":
    test_database_otp()