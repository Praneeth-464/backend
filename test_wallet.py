import requests
import json
from datetime import datetime
from uuid import UUID

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_wallet_functionality():
    """
    Test the wallet functionality
    """
    print("Testing wallet functionality...")
    
    # You'll need a valid user ID
    print(f"\n[{datetime.now()}] You'll need a valid user ID to test wallet functionality.")
    user_id = input("Enter a valid user ID: ")
    
    # Test getting wallet balance
    print(f"\n[{datetime.now()}] Getting wallet balance...")
    try:
        response = requests.get(f"{BASE_URL}/wallet/balance/{user_id}")
        print(f"Get Balance Status Code: {response.status_code}")
        print(f"Get Balance Response: {response.json()}")
    except Exception as e:
        print(f"Error getting wallet balance: {e}")
    
    # Test creating a credit transaction
    print(f"\n[{datetime.now()}] Creating a credit transaction...")
    credit_transaction = {
        "user_id": user_id,
        "amount": 50.0,
        "transaction_type": "credit",
        "description": "Promotional credit"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/wallet/transaction", json=credit_transaction)
        print(f"Credit Transaction Status Code: {response.status_code}")
        print(f"Credit Transaction Response: {response.json()}")
    except Exception as e:
        print(f"Error creating credit transaction: {e}")
    
    # Test creating a debit transaction
    print(f"\n[{datetime.now()}] Creating a debit transaction...")
    debit_transaction = {
        "user_id": user_id,
        "amount": 10.0,
        "transaction_type": "debit",
        "description": "Ride payment"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/wallet/transaction", json=debit_transaction)
        print(f"Debit Transaction Status Code: {response.status_code}")
        print(f"Debit Transaction Response: {response.json()}")
    except Exception as e:
        print(f"Error creating debit transaction: {e}")
    
    # Test getting transaction history
    print(f"\n[{datetime.now()}] Getting transaction history...")
    try:
        response = requests.get(f"{BASE_URL}/wallet/transactions/{user_id}")
        print(f"Get Transactions Status Code: {response.status_code}")
        print(f"Get Transactions Response: {response.json()}")
    except Exception as e:
        print(f"Error getting transaction history: {e}")

if __name__ == "__main__":
    test_wallet_functionality()