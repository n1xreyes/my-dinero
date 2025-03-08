from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from db.session import SessionLocal
from db.schemas import UserCreate, UserResponse
from db.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

def hash_password(password: str) -> str:
    # For production use a secure method such as bcrypt or passlib.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
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