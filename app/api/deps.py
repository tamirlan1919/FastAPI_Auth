from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.database import get_async_session
from app.db.models import User
from app.repositories.user_repo import UserRepo
from app.shemas.token import TokenPayload


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



def require_role(role: str):
    pass
