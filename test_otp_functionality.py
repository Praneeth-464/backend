import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_otp_functionality():
    """
    Test the OTP functionality
    """
    print("Testing OTP functionality...")
    
    # Test user data (use an existing verified user)
    user_email = "test@example.com"
    
    # 1. Request OTP
    print("\n1. Requesting OTP...")
    otp_request_data = {
        "email": user_email
    }
    otp_response = requests.post(f"{BASE_URL}/auth/request-otp", json=otp_request_data)
    print(f"OTP Request Status Code: {otp_response.status_code}")
    print(f"OTP Request Response: {otp_response.json()}")
    
    if otp_response.status_code != 200:
        print("OTP request failed. Exiting test.")
        return
    
    # 2. Verify OTP (you'll need to check your email for the actual OTP)
    print("\n2. Verifying OTP...")
    print("Please check your email for the OTP code and enter it below:")
    otp_code = input("Enter OTP: ")
    
    otp_verify_data = {
        "email": user_email,
        "otp": otp_code
    }
    verify_response = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_verify_data)
    print(f"OTP Verify Status Code: {verify_response.status_code}")
    print(f"OTP Verify Response: {verify_response.json()}")
    
    if verify_response.status_code == 200:
        print("\nOTP verification successful!")
        print("You can now proceed with login.")
    else:
        print("\nOTP verification failed.")

if __name__ == "__main__":
    test_otp_functionality()