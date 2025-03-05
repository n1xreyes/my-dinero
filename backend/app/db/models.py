from sqlalchemy import Column, String, Boolean, DateTime, DECIMAL, ForeignKey, UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    currency = Column(String, default='CAD')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    bank_accounts = relationship("BankAccount", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    institution_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(DECIMAL, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    bank_account_id = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions")
