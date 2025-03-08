import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

from main import app
from db.schemas import UserCreate, UserResponse
from db.models import User
from api.routes.users import get_db

client = TestClient(app)

# Mock the database session
@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    yield db

# Override dependency
app.dependency_overrides[get_db] = lambda: mock_db()

# Test user registration
def test_register_user_success(mock_db):
    # avoid direct calls of the fixture
    app.dependency_overrides[get_db] = lambda: mock_db

    # Mock the database query and commit
    mock_db.query(User).filter().first.return_value = None
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "currency": "CAD"
    }
    response = client.post("/users/register", json=user_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] == user_data["email"]

# Use the fixture properly in the test
def test_register_user_already_exists(mock_db):
    # avoid direct calls of the fixture
    app.dependency_overrides[get_db] = lambda: mock_db

    # Mock a user already exists in the database
    mock_user = User(
        email="test@example.com",
        password_hash="hashedpw",
        name="Test User",
        currency="CAD"
    )
    mock_db.query(User).filter().first.return_value = mock_user

    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "currency": "CAD"
    }

    response = client.post("/users/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
