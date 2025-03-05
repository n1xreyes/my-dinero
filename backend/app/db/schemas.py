from pydantic import BaseModel, EmailStr, UUID4
import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    currency: Optional[str] = "CAD"

class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    name: Optional[str]
    currency: str
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class BankAccountCreate(BaseModel):
    institution_name: str
    account_type: str
    balance: float

class BankAccountResponse(BankAccountCreate):
    id: UUID4
    user_id: UUID4
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    bank_account_id: UUID4
    description: str
    amount: float
    date: Optional[datetime.datetime] = None

class TransactionResponse(TransactionCreate):
    id: UUID4
    user_id: UUID4
    class Config:
        from_attributes = True