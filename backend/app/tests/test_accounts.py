import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from uuid import uuid4, UUID
from datetime import datetime, timezone

from main import app
from db.models import User, BankAccount
from api.routes.accounts import get_db

client = TestClient(app)

# Fixture to provide a MagicMock for the database session.
@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    yield db

# Automatically clear dependency overrides after each test.
@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_create_account_success(mock_db):
    # Override dependency to use our mock_db.
    app.dependency_overrides[get_db] = lambda: mock_db

    # Simulate that the user exists.
    fake_user_id = uuid4()
    fake_user = User(
        id=fake_user_id,
        email="user@example.com",
        password_hash="hashed",
        name="User",
        currency="CAD",
        created_at=datetime.now(timezone.utc)
    )
    # When querying for the user, return fake_user.
    mock_db.query(User).filter().first.return_value = fake_user

    # Prepare expected values for the created bank account.
    fake_account_id = uuid4()
    fake_created_at = datetime.now(timezone.utc)

    # Simulate the behavior of db.refresh by assigning values to the instance.
    def fake_refresh(instance):
        instance.id = fake_account_id
        instance.user_id = fake_user_id
        instance.institution_name = "Test Bank"
        instance.account_type = "Checking"
        instance.balance = 100.0
        instance.created_at = fake_created_at

    mock_db.refresh.side_effect = fake_refresh
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    account_data = {
        "institution_name": "Test Bank",
        "account_type": "Checking",
        "balance": 100.0
    }
    response = client.post(f"/accounts/?user_id={fake_user_id}", json=account_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["institution_name"] == account_data["institution_name"]
    # Verify that the returned id is a valid UUID.
    try:
        UUID(data["id"])
    except ValueError:
        pytest.fail("Invalid UUID format for id")
    assert "created_at" in data

def test_create_account_user_not_found(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    # Simulate that the user is not found.
    mock_db.query(User).filter().first.return_value = None

    fake_user_id = uuid4()
    account_data = {
        "institution_name": "Test Bank",
        "account_type": "Checking",
        "balance": 100.0
    }
    response = client.post(f"/accounts/?user_id={fake_user_id}", json=account_data)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
