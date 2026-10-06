import pytest

def test_register_success(client, user_payload):
    response = client.post("/auth/register", json=user_payload)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == 'tima@test.com'
    assert data["username"] == 'testuser'
    assert 'password' not in data
    assert 'hashed_password' not in data


def test_register_duplicate(client, user_payload):
    response = client.post("/auth/register", json=user_payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}



@pytest.mark.parametrize('payload', [
    {
        'username': 'ab',
        "email": "alice@example.com",
        "username": "super-key123",
    },
    {
        'username': 'alice',
        "email": "not-a-email",
        "username": "super-key123",
    },
    {
        'username': 'alice',
        "email": "test@mail.ru",
        "username": "123",
    },
])
def test_invalid_register(client, payload):
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422


def test_login_success(client, registered_user):
    response = client.post("/auth/token", data={
        "username": registered_user["username"],
        "password": registered_user["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_invalid_login(client):
    response = client.post("/auth/token", data={
        'username': 'test',
        'password': 'test',
    })
    assert response.status_code == 401


def test_get_me(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_valid_me(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == 'testuser'

