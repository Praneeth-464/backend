import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def debug_otp_flow():
    """
    Debug the OTP flow step by step
    """
    print("Debugging OTP flow...")
    
    # Test user data (use an existing verified user)
    user_email = input("Enter your email: ")
    
    # 1. Request OTP
    print(f"\n[{datetime.now()}] 1. Requesting OTP for {user_email}...")
    otp_request_data = {
        "email": user_email
    }
    try:
        otp_response = requests.post(f"{BASE_URL}/auth/request-otp", json=otp_request_data)
        print(f"OTP Request Status Code: {otp_response.status_code}")
        print(f"OTP Request Response: {otp_response.json()}")
        
        if otp_response.status_code != 200:
            print("OTP request failed. Exiting debug.")
            return
    except Exception as e:
        print(f"Error requesting OTP: {e}")
        return
    
    # 2. Wait for user to check email
    print(f"\n[{datetime.now()}] 2. Please check your email for the OTP code.")
    print("The OTP will expire in 30 minutes.")
    otp_code = input("Enter OTP (or 'skip' to test expiration): ")
    
    if otp_code.lower() == 'skip':
        print("Testing OTP expiration... please wait 30 minutes and then run this script again.")
        return
    
    # 3. Verify OTP
    print(f"\n[{datetime.now()}] 3. Verifying OTP...")
    otp_verify_data = {
        "email": user_email,
        "otp": otp_code
    }
    try:
        verify_response = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_verify_data)
        print(f"OTP Verify Status Code: {verify_response.status_code}")
        print(f"OTP Verify Response: {verify_response.json()}")
        
        if verify_response.status_code == 200:
            print("\nOTP verification successful!")
        else:
            print("\nOTP verification failed.")
    except Exception as e:
        print(f"Error verifying OTP: {e}")

if __name__ == "__main__":
    debug_otp_flow()