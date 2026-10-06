import pytest
from fastapi.testclient import TestClient

from app.main import app # Импортируем наше FastAPI приложение
from app.repositories.user_repo import user_repo

@pytest.fixture(scope="module") # scope="module" — фикстура создастся один раз для всех тестов в модуле
def client():
    """ Фикстура для создания TestClient. """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_payload():
    return  {
        "username": "testuser",
        "email": "tima@test.com",
        "password": "Super-key123",
    }


@pytest.fixture
def registered_user(client, user_payload):
    client.post('/auth/register', json=user_payload)
    return user_payload

@pytest.fixture
def auth_headers(client, user_payload):
    response = client.post('/auth/token', data={
        "username": user_payload["username"],
        "password": user_payload["password"],
    })

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
