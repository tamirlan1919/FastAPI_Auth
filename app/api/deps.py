from typing import Annotated, Any

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.clients.yandex_oauth import YandexOauthClient
from app.core.security import decode_token
from app.db.database import get_async_session
from app.db.models import User
from app.db.redis_db import get_redis
from app.repositories.post_repo import PostRepo
from app.repositories.profile_repo import ProfileRepo
from app.repositories.tag_repo import TagRepo
from app.repositories.user_repo import UserRepo
from app.schemas.token import TokenPayload
from app.broker.rabbit import EventPublisher, get_publisher


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'Не удалось подтвердить учетные данные',
    headers={"WWW-Authenticate": "Bearer"},

)


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session)


UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]

PublisherDep = Annotated[EventPublisher, Depends(get_publisher)]

def get_post_repo(session: SessionDep) -> PostRepo:
    return PostRepo(session)


PostRepoDep = Annotated[PostRepo, Depends(get_post_repo)]


def get_tag_repo(session: SessionDep) -> TagRepo:
    return TagRepo(session)


TagRepoDep = Annotated[TagRepo, Depends(get_tag_repo)]


def get_profile_repo(session: SessionDep) -> ProfileRepo:
    return ProfileRepo(session)


ProfileRepoDep = Annotated[ProfileRepo, Depends(get_profile_repo)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: UserRepoDep,
) -> User:
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    data = TokenPayload(**payload)
    if data.sub is None:
        raise credentials_exception
    user = await user_repo.get_by_username(data.sub)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


RedisDep = Annotated[Redis, Depends(get_redis)]


def _integration(request: Request, name: str, title: str):
    client = getattr(request.app.state, name, None)
    if client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail = f'{title} не настроен')
    return client

def get_yandex_oauth(request: Request) -> Any | None:
    return _integration(request, 'yandex_oauth', 'Вход через Яндекс')

def get_yandex_disk(request: Request) -> Any | None:
    return _integration(request, 'yandex_disk', 'Яндекс Диск')

YandexOauthDep = Annotated[YandexOauthClient, Depends(get_yandex_oauth)]


def require_role(role: str):
    pass
