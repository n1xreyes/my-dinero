from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
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
    bank_name: str
    account_type: Optional[str] = None
    account_number: Optional[str] = None
    balance: float = 0.00
    is_manual: bool = False

class BankAccountResponse(BaseModel):
    id: UUID4
    bank_name: str
    account_type: Optional[str]
    account_number: Optional[str]
    balance: float
    is_manual: bool
    last_updated_at: datetime.datetime

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    bank_account_id: UUID4
    amount: float
    category_id: Optional[UUID4] = None
    merchant_name: Optional[str] = None
    transaction_date: datetime.datetime
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: UUID4
    bank_account_id: UUID4
    amount: float
    category_id: Optional[UUID4]
    merchant_name: Optional[str]
    transaction_date: datetime.datetime
    description: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True
