from app.core.security import hash_password, verify_password
from app.db.models import User
from app.repositories.user_repo import UserRepo

async def register_user(user_repo: UserRepo, username: str, email: str, password: str) -> User:
    if await user_repo.get_by_username(username):
        raise ValueError('Username already exists')
    return await user_repo.create(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        roles=['user']
    )


async def authenticate_user(user_repo: UserRepo, username: str, password: str) -> User | None:
    user = await user_repo.get_by_username(username)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user
