from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.core.security import decode_token
from app.models.user import User
from app.repositories.user_repo import user_repo
from app.shemas.token import TokenPayload


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'Не удалось подтвердить учетные данные',
    headers={"WWW-Authenticate": "Bearer"},

)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User | None:
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    data = TokenPayload(**payload)
    if data.sub is None:
        raise credentials_exception

    user = user_repo.get_by_username(data.sub)
    if user is None:
        raise credentials_exception
    return user


def require_role(role: str):
    pass
