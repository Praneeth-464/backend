import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_user_signup_and_verification():
    """
    Test the complete user signup and email verification flow
    """
    print("Testing user signup and email verification flow...")
    
    # Test user data
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    # 1. Sign up a new user
    print("\n1. Signing up new user...")
    signup_response = requests.post(f"{BASE_URL}/auth/signup/user", json=user_data)
    print(f"Signup Status Code: {signup_response.status_code}")
    print(f"Signup Response: {signup_response.json()}")
    
    if signup_response.status_code != 200:
        print("Signup failed. Exiting test.")
        return
    
    # 2. Try to login (should fail because email is not verified)
    print("\n2. Attempting to login (should fail)...")
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Login Status Code: {login_response.status_code}")
    print(f"Login Response: {login_response.json()}")
    
    print("\n3. To test email verification:")
    print("- Check your email for the verification link")
    print("- Extract the token from the link")
    print("- Call the verify-email endpoint with the token")
    print("- Try logging in again")

if __name__ == "__main__":
    test_user_signup_and_verification()