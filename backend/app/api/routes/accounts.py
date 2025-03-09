from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from db.session import SessionLocal
from db.schemas import BankAccountCreate, BankAccountResponse
from db.models import BankAccount, User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/", response_model=BankAccountResponse)
def create_account(
        account: BankAccountCreate,
        user_id: UUID = Query(..., description="ID of the user who owns this account"),
        db: Session = Depends(get_db)
):
    # Ensure the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_account = BankAccount(
        user_id=user_id,
        institution_name=account.institution_name,
        account_type=account.account_type,
        balance=account.balance
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
