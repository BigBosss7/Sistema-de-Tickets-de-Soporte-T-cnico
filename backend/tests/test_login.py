from fastapi.testclient import TestClient 

from app.main import app

client = TestClient(app)

def test_user_fixture(test_user):

    assert test_user["name"] == "Test User"

    assert test_user["email"] == "test@example.com"



def test_register_user(test_user):

    response = client.post(
        "/user",
        json=test_user
    )

    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
    assert response.json()["name"] == test_user ["name"]