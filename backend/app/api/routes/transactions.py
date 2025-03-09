from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from db.session import SessionLocal
from db.schemas import TransactionCreate, TransactionResponse
from db.models import Transaction, BankAccount

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_transaction(
        transaction: TransactionCreate,
        user_id: UUID = Query(..., description="ID of the user creating the transaction"),
        db: Session = Depends(get_db)
):
    # Ensure the bank account exists (optionally, you might also verify that it belongs to the user)
    account = db.query(BankAccount).filter(BankAccount.id == transaction.bank_account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db_transaction = Transaction(
        user_id=user_id,
        bank_account_id=transaction.bank_account_id,
        description=transaction.description,
        amount=transaction.amount,
        date=transaction.date  # If None, the model default will be used
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
