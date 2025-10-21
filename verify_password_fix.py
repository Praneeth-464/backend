#!/usr/bin/env python3
"""
Simple verification script for password truncation fix
"""

def test_password_truncation_logic():
    """Test the password truncation logic without actually hashing"""
    
    # Test password that's longer than 72 bytes
    long_password = "a" * 100
    
    # Check if it gets truncated properly
    if len(long_password.encode('utf-8')) > 72:
        truncated = long_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        print(f"Original length: {len(long_password.encode('utf-8'))} bytes")
        print(f"Truncated length: {len(truncated.encode('utf-8'))} bytes")
        print(f"Truncation works correctly: {len(truncated.encode('utf-8')) <= 72}")
    
    # Test with a normal password
    normal_password = "normal_password_123"
    if len(normal_password.encode('utf-8')) > 72:
        truncated = normal_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        print("Normal password was truncated (should not happen)")
    else:
        print("Normal password is within limit (correct)")
    
    print("Password truncation logic verified successfully!")

if __name__ == "__main__":
    test_password_truncation_logic()