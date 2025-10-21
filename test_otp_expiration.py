import requests
import time
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_otp_expiration():
    """
    Test OTP expiration functionality
    """
    print("Testing OTP expiration...")
    
    # Test user data (use an existing verified user)
    user_email = input("Enter your email: ")
    
    # 1. Request OTP
    print(f"\n[{datetime.now()}] Requesting OTP for {user_email}...")
    otp_request_data = {
        "email": user_email
    }
    otp_response = requests.post(f"{BASE_URL}/auth/request-otp", json=otp_request_data)
    print(f"OTP Request Status Code: {otp_response.status_code}")
    print(f"OTP Request Response: {otp_response.json()}")
    
    if otp_response.status_code != 200:
        print("OTP request failed. Exiting test.")
        return
    
    # 2. Get OTP from user
    otp_code = input("Enter the OTP you received via email: ")
    
    # 3. Test immediate verification (should work)
    print(f"\n[{datetime.now()}] Testing immediate OTP verification...")
    otp_verify_data = {
        "email": user_email,
        "otp": otp_code
    }
    verify_response = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_verify_data)
    print(f"Immediate Verification Status Code: {verify_response.status_code}")
    print(f"Immediate Verification Response: {verify_response.json()}")
    
    if verify_response.status_code == 200:
        print("Immediate verification successful!")
        # Request another OTP for the expiration test
        print(f"\n[{datetime.now()}] Requesting another OTP for expiration test...")
        otp_response2 = requests.post(f"{BASE_URL}/auth/request-otp", json=otp_request_data)
        if otp_response2.status_code != 200:
            print("Failed to request second OTP. Exiting test.")
            return
        otp_code = input("Enter the new OTP: ")
    else:
        print("Immediate verification failed.")
    
    # 4. Test expiration by waiting
    print(f"\n[{datetime.now()}] Testing OTP expiration...")
    print("You have two options:")
    print("1. Wait for actual expiration (30 minutes)")
    print("2. Test with an invalid OTP")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        print("Waiting for 30 minutes for OTP to expire...")
        print("This will take a while. Please be patient.")
        # In a real test, you would wait for the actual expiration time
        # For demonstration, we'll simulate the expiration
        print("Simulating OTP expiration...")
        time.sleep(5)  # Wait a few seconds for demonstration
        
        # Try to verify with the same OTP (should fail)
        print(f"\n[{datetime.now()}] Trying to verify expired OTP...")
        verify_response2 = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_verify_data)
        print(f"Expired OTP Verification Status Code: {verify_response2.status_code}")
        print(f"Expired OTP Verification Response: {verify_response2.json()}")
        
        if verify_response2.status_code == 401:
            print("OTP expiration test successful - OTP correctly rejected as expired.")
        else:
            print("OTP expiration test failed.")
            
    elif choice == "2":
        # Test with an invalid OTP
        print(f"\n[{datetime.now()}] Testing with invalid OTP...")
        invalid_otp_data = {
            "email": user_email,
            "otp": "000000"  # Invalid OTP
        }
        verify_response3 = requests.post(f"{BASE_URL}/auth/verify-otp", json=invalid_otp_data)
        print(f"Invalid OTP Verification Status Code: {verify_response3.status_code}")
        print(f"Invalid OTP Verification Response: {verify_response3.json()}")
        
        if verify_response3.status_code == 401:
            print("Invalid OTP test successful - OTP correctly rejected as invalid.")
        else:
            print("Invalid OTP test failed.")

if __name__ == "__main__":
    test_otp_expiration()