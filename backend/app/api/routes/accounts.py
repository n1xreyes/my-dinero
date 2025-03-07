from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.schemas import BankAccountCreate, BankAccountResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/", response_model=BankAccountResponse)
def create_account(account: BankAccountCreate, db: Session = Depends(get_db)):
    # Placeholder logic: Implement account creation and association with a user.
    return {"message": "Bank account created!"}
