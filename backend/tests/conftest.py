import pytest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app 

client = TestClient(app)


@pytest.fixture
def test_user():
    return {
        "name": "Test User",
        "email": f"test_{uuid4().hex}@example.com",
        "password": "123456",
        "role": "USER"
    }

@pytest.fixture
def auth_user(test_user):
    create_response = client.post(
        "/user",
        json=test_user
    )

    created_user = create_response.json()

    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    access_token = login_response.json()["access_token"]

    return {
        "headers": {
        "Authorization": f"Bearer {access_token}"
    },
    "user": created_user
    }