from fastapi.testclient import TestClient 

from app.main import app

client = TestClient(app)

def test_user_fixture(test_user):

    assert test_user["name"] == "Test User"

    assert "@example.com" in test_user["email"]


def test_register_user(test_user):

    response = client.post(
        "/user",
        json=test_user
    )

    response = client.post(
        "auth/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    