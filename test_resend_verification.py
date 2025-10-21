import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_resend_verification():
    """
    Test the resend verification email functionality
    """
    print("Testing resend verification email functionality...")
    
    # Test data
    resend_data = {
        "email": "test@example.com"
    }
    
    # Resend verification email
    print("\nResending verification email...")
    resend_response = requests.post(f"{BASE_URL}/auth/resend-verification", json=resend_data)
    print(f"Resend Status Code: {resend_response.status_code}")
    print(f"Resend Response: {resend_response.json()}")

if __name__ == "__main__":
    test_resend_verification()