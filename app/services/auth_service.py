from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repo import user_repo

def register_user(username: str, email: str, password: str) -> User:
    if user_repo.get_by_username(username):
        raise ValueError('Username already exists')
    return user_repo.create(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        roles=['user']
    )


def authenticate_user(username: str, password: str) -> User:
    user = user_repo.get_by_username(username)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user
