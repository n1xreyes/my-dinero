from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from api.dependencies import get_db  # Centralized dependency
from db.schemas import TransactionCreate, TransactionResponse
from db.models import Transaction, BankAccount

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_transaction(
        transaction: TransactionCreate,
        user_id: UUID = Query(..., description="ID of the user creating the transaction"),
        db: Session = Depends(get_db)
):
    # Verify that the bank account exists
    account = db.query(BankAccount).filter(BankAccount.id == transaction.bank_account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db_transaction = Transaction(
        user_id=user_id,
        bank_account_id=transaction.bank_account_id,
        description=transaction.description,
        amount=transaction.amount,
        date=transaction.date  # If None, model default will be used.
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
