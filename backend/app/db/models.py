from sqlalchemy import Column, String, Boolean, DateTime, DECIMAL, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

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
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bank_name = Column(String, nullable=False)
    account_type = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    balance = Column(DECIMAL(12,2), default=0.00)
    is_manual = Column(Boolean, default=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    plaid_access_token = Column(String, nullable=True)
    last_synced_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bank_account_id = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(12,2), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    merchant_name = Column(String, nullable=True)
    transaction_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions")
