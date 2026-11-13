import secrets

from app.core.security import hash_password
from app.db.models import User
from app.repositories.user_repo import UserRepo
from app.schemas.yandex import YandexProfile


class YandexEmailRequired(Exception):
    pass


async def login_or_register(user_repo: UserRepo, profile: YandexProfile):
    if not profile.default_email:
        raise YandexEmailRequired('Яндекс не передал email')
    email = profile.default_email
    user = await user_repo.get_by_email(email)
    if user is not None:
        return user

    username = profile.login

    if await user_repo.get_by_username(username) is not None:
        username = f'{profile.login}_ya{profile.id[-4:]}'

    return await user_repo.create(
        username=username,
        email=email,
        hashed_password=hash_password(secrets.token_urlsafe(32)),
        roles=['user']
    )

