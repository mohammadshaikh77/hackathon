from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.deps import get_current_active_user
from app.models.models import User
from app.schemas.schemas import WalletTransaction

router = APIRouter()


@router.get("/balance")
def get_wallet_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current wallet balance"""
    return {"balance": current_user.wallet_balance, "currency": "USD"}


@router.post("/deposit")
def deposit_to_wallet(
    transaction: WalletTransaction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deposit money to wallet (simulation)"""
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    current_user.wallet_balance += transaction.amount
    db.commit()
    
    return {
        "message": "Deposit successful",
        "new_balance": current_user.wallet_balance,
        "transaction": transaction.description
    }


@router.post("/withdraw")
def withdraw_from_wallet(
    transaction: WalletTransaction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Withdraw money from wallet (simulation)"""
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    if current_user.wallet_balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    current_user.wallet_balance -= transaction.amount
    db.commit()
    
    return {
        "message": "Withdrawal successful",
        "new_balance": current_user.wallet_balance,
        "transaction": transaction.description
    }


@router.post("/transfer")
def transfer_funds(
    recipient_id: int,
    transaction: WalletTransaction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Transfer funds to another user (simulation)"""
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    if current_user.wallet_balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    recipient = db.query(User).filter(User.id == recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # Transfer
    current_user.wallet_balance -= transaction.amount
    recipient.wallet_balance += transaction.amount
    db.commit()
    
    return {
        "message": "Transfer successful",
        "new_balance": current_user.wallet_balance,
        "recipient": recipient.username,
        "amount": transaction.amount
    }
