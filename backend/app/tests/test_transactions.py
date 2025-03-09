import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from uuid import uuid4, UUID
from datetime import datetime, timezone

from main import app
from db.models import BankAccount, Transaction
from api.routes.transactions import get_db

client = TestClient(app)

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    yield db

@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_create_transaction_success(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

    # Simulate that the bank account exists.
    fake_account_id = uuid4()
    fake_user_id = uuid4()
    fake_account = BankAccount(
        id=fake_account_id,
        user_id=fake_user_id,
        institution_name="Test Bank",
        account_type="Checking",
        balance=100.0,
        created_at=datetime.now(timezone.utc)
    )
    mock_db.query(BankAccount).filter().first.return_value = fake_account

    # Prepare expected values for the created transaction.
    fake_transaction_id = uuid4()
    fake_created_date = datetime.now(timezone.utc)

    def fake_refresh(instance):
        instance.id = fake_transaction_id
        instance.user_id = fake_user_id
        instance.bank_account_id = fake_account_id
        instance.description = "Test transaction"
        instance.amount = 50.0
        instance.date = fake_created_date

    mock_db.refresh.side_effect = fake_refresh
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    transaction_data = {
        "bank_account_id": str(fake_account_id),
        "description": "Test transaction",
        "amount": 50.0
    }
    response = client.post(f"/transactions/?user_id={fake_user_id}", json=transaction_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["description"] == transaction_data["description"]
    try:
        UUID(data["id"])
    except ValueError:
        pytest.fail("Invalid UUID format for transaction id")
    assert "date" in data

def test_create_transaction_account_not_found(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    # Simulate that the bank account is not found.
    mock_db.query(BankAccount).filter().first.return_value = None

    fake_user_id = uuid4()
    transaction_data = {
        "bank_account_id": str(uuid4()),
        "description": "Test transaction",
        "amount": 50.0
    }
    response = client.post(f"/transactions/?user_id={fake_user_id}", json=transaction_data)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Bank account not found"
