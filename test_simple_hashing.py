#!/usr/bin/env python3
"""
Test script to verify simple password hashing without 72-byte limitation
"""

from app.utils.jwt_utils import get_password_hash, verify_password

def test_simple_hashing():
    """Test simple password hashing without 72-byte limitation"""
    
    # Test with a very long password
    long_password = "a" * 1000  # 1000 characters, well over 72 bytes
    print(f"Testing with password of {len(long_password)} characters")
    
    try:
        # Hash the long password
        hashed = get_password_hash(long_password)
        print(f"Password hashed successfully")
        
        # Verify the password
        is_valid = verify_password(long_password, hashed)
        print(f"Password verification: {'SUCCESS' if is_valid else 'FAILED'}")
        
        # Test with a wrong password
        is_valid_wrong = verify_password(long_password + "wrong", hashed)
        print(f"Wrong password verification: {'FAILED (this is good!)' if not is_valid_wrong else 'UNEXPECTED SUCCESS'}")
        
        if is_valid and not is_valid_wrong:
            print("Simple hashing approach works correctly!")
        else:
            print("There was an issue with the hashing approach")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        print("The simple hashing approach may not be working correctly")

if __name__ == "__main__":
    test_simple_hashing()