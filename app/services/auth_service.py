from app.core.security import hash_password, verify_password
from app.db.models import User
from app.repositories.user_repo import UserRepo
from app.core.errors import ConflictError


class UserAlreadyExist(ConflictError):
    code = 'user_already_exist'

async def register_user(user_repo: UserRepo, username: str, email: str, password: str) -> User:
    if await user_repo.get_by_username(username):
        raise UserAlreadyExist('Пользователь с таким именем уже существует')
    if await user_repo.get_by_email(email):
        raise UserAlreadyExist('Пользователь с таким email уже существует')
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
