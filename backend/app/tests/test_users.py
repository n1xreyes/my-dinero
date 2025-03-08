import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from datetime import datetime, timezone
from uuid import uuid4, UUID

from main import app
from db.schemas import UserCreate, UserResponse
from db.models import User
from api.routes.users import get_db

client = TestClient(app)

# Fixture to provide a MagicMock for the database session.
@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    yield db

# Test for successful user registration.
def test_register_user_success(mock_db):
    # Override the dependency to return our mock_db instance.
    app.dependency_overrides[get_db] = lambda: mock_db

    # Ensure that no user exists with the given email.
    mock_db.query(User).filter().first.return_value = None

    # Create fake values that we expect to be set after commit/refresh.
    fake_id = uuid4()
    fake_created_at = datetime.now(timezone.utc)

    # Define a side_effect for refresh to simulate the ORM behavior:
    # When db.refresh(db_user) is called, assign the expected attributes to the instance.
    def fake_refresh(instance):
        instance.id = fake_id
        instance.email = "test@example.com"
        instance.name = "Test User"
        instance.currency = "CAD"
        instance.created_at = fake_created_at

    mock_db.refresh.side_effect = fake_refresh
    # No-op for add and commit.
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "currency": "CAD"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200, response.text

    response_data = response.json()
    # Validate the response fields.
    assert response_data["email"] == user_data["email"]
    # Check that the id is a valid UUID string.
    try:
        UUID(response_data["id"])
    except ValueError:
        pytest.fail("Invalid UUID format for id")
    assert "created_at" in response_data

# Test for duplicate user registration.
def test_register_user_already_exists(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

    # Simulate that a user already exists by having query(...).first() return a User.
    existing_user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashedpw",
        name="Test User",
        currency="CAD",
        created_at=datetime.now(timezone.utc)
    )
    mock_db.query(User).filter().first.return_value = existing_user

    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "currency": "CAD"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Email already registered"

# Clear dependency overrides after tests.
@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()
