import secrets

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse

from app.api.deps import RedisDep, UserRepoDep, YandexOauthDep
from app.clients.yandex_oauth import YandexOauthError
from app.core.security import create_access_token
from app.schemas.token import Token
from app.services.yandex_auth import YandexEmailRequired, login_or_register


router = APIRouter(prefix='/auth/yandex', tags=['Вход через Yandex'])

STATE_TTL=600

@router.get('/login')
async def yandex_login(yandex: YandexOauthDep, redis: RedisDep):
    state = secrets.token_urlsafe(32)
    await redis.set(f'oauth:state:{state}', '1', ex=STATE_TTL)
    return RedirectResponse(yandex.authorize(state))

@router.get('/callback', response_model=Token)
async def yandex_callback(
        user_repo: UserRepoDep,
        yandex: YandexOauthDep,
        redis: RedisDep,
        code: str | None = None,
        state: str | None = None,
        error: str | None = None,
        error_description: str | None = None,

):
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{error_description}')

    if not code or not state or not await redis.get(f'oauth:state:{state}'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'неверный или устаревший state'
                                                                            f' начните вход заново')

    try:
        token = await yandex.exchange_code(code)
        profile = await yandex.get_profile(token.access_token)
    except YandexOauthError:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, 'Не удалось войти через яндекс')

    try:
        user = await login_or_register(user_repo, profile)
    except YandexEmailRequired:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Разрешите приложению доступ к email')
    return Token(access_token=create_access_token(data={'sub': user.username}))
