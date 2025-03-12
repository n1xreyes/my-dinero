from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from api.dependencies import get_db  # Centralized dependency
from db.schemas import UserCreate, UserResponse
from db.models import User

router = APIRouter()

def hash_password(password: str) -> str:
    # Use a secure hash function (for production, consider bcrypt via passlib)
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_pw,
        name=user.name,
        currency=user.currency
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
