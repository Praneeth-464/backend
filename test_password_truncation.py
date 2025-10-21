#!/usr/bin/env python3
"""
Test script to verify password truncation for bcrypt compatibility
"""

from app.utils.jwt_utils import get_password_hash, verify_password

def test_password_truncation():
    """Test password truncation for bcrypt compatibility"""
    
    # Test with a short password
    short_password = "short123"
    hashed_short = get_password_hash(short_password)
    assert verify_password(short_password, hashed_short)
    print("Short password test passed")
    
    # Test with a password that's exactly 72 bytes
    exact_password = "a" * 72
    hashed_exact = get_password_hash(exact_password)
    assert verify_password(exact_password, hashed_exact)
    print("Exact 72-byte password test passed")
    
    # Test with a password that exceeds 72 bytes
    long_password = "a" * 100
    hashed_long = get_password_hash(long_password)
    # Should still verify with the original long password
    assert verify_password(long_password, hashed_long)
    print("Long password truncation test passed")
    
    # Test with unicode characters
    unicode_password = "🚀" * 50  # Each rocket emoji is 4 bytes in UTF-8
    hashed_unicode = get_password_hash(unicode_password)
    assert verify_password(unicode_password, hashed_unicode)
    print("Unicode password test passed")
    
    print("All password truncation tests passed!")

if __name__ == "__main__":
    test_password_truncation()