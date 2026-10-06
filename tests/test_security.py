from app.core.security import (
    hash_password,
    decode_token,
    verify_password,
    create_access_token
)


def test_hash_password():
    hashed = hash_password("superkey")
    assert hashed != "superkey"
    assert verify_password("superkey", hashed)
    assert not verify_password("", hashed)


def test_jwt():
    token = create_access_token({"sub": "testuser", 'roles': ['user']})
    payload = decode_token(token)
    assert payload['sub'] == 'testuser'
    assert payload['roles'] == ['user']




