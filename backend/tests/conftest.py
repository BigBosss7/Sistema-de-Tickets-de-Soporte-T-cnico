import pytest

@pytest.fixture
def test_user():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "123456",
        "role": "USER"
    }