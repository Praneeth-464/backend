from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List
from ..schemas import WalletTransactionCreate, WalletTransaction
from ..crud import create_wallet_transaction, get_wallet_balance, get_wallet_transactions, get_user_by_email
from ..utils.datetime_serializer import simple_datetime_handler
from ..utils.auth_utils import get_current_user
import traceback

router = APIRouter()

@router.get("/balance")
async def get_wallet_balance_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Get wallet balance for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        balance = get_wallet_balance(user.id)
        return {"user_id": str(user.id), "balance": balance}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_wallet_balance_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving wallet balance: {str(e)}")

@router.post("/transaction", response_model=WalletTransaction)
async def create_wallet_transaction_endpoint(transaction: WalletTransactionCreate, current_user_email: str = Depends(get_current_user)):
    """
    Create a wallet transaction (credit or debit) for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use the authenticated user's ID if no user_id is provided in the request
        # If user_id is provided, ensure it matches the authenticated user's ID
        if transaction.user_id is None:
            user_id = user.id
        elif transaction.user_id != user.id:
            raise HTTPException(status_code=403, detail="You can only create transactions for your own wallet")
        else:
            user_id = transaction.user_id
        
        # Validate transaction type
        if transaction.transaction_type not in ["credit", "debit"]:
            raise HTTPException(status_code=400, detail="Transaction type must be 'credit' or 'debit'")
        
        wallet_transaction = create_wallet_transaction(
            user_id,
            transaction.amount,
            transaction.transaction_type,
            transaction.description
        )
        
        if not wallet_transaction:
            raise HTTPException(status_code=500, detail="Error creating wallet transaction")
        
        return simple_datetime_handler(wallet_transaction)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_wallet_transaction_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error creating wallet transaction: {str(e)}")

@router.get("/transactions", response_model=List[WalletTransaction])
async def get_wallet_transactions_endpoint(current_user_email: str = Depends(get_current_user)):
    """
    Get transaction history for the authenticated user
    """
    try:
        # Get the current user
        user = get_user_by_email(current_user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get transactions for the current user
        transactions = get_wallet_transactions(user.id)
        return transactions
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_wallet_transactions_endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving wallet transactions: {str(e)}")