import json

from fastapi import APIRouter, HTTPException, Response
from app.clients.github import get_user
from app.schemas.github import GithubUser
import httpx
from app.api.deps import RedisDep

router = APIRouter(prefix="/github", tags=["github"])

GITHUB_CACHE_TTL = 600  # секунд


@router.get("/{username}", response_model=GithubUser)
async def get_github_user(username: str, redis: RedisDep, response: Response):
    key = f'github:card:{username.lower()}'

    # Смотрим в кеш
    cached = await redis.get(key)
    if cached is not None:
        response.headers['X-Cache'] = 'HIT'
        return json.loads(cached)

    try:
        raw = await get_user(username)
    except httpx.TimeoutException:
        # Ошибка таймаута
        raise HTTPException(status_code=504, detail="Внешний сервис не ответил вовремя.")
    except httpx.ConnectError:
        # Ошибка соединения
        raise HTTPException(status_code=503, detail="Не удалось подключиться к внешнему сервису.")
    except httpx.HTTPStatusError as e:
        # Ошибка со статусом 4xx или 5xx
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Внешний сервис вернул ошибку: {e.response.text}"
        )

    # Ответ GitHub -> только нужные поля -> JSON-строка в Redis на 10 минут
    user = GithubUser.model_validate(raw)
    await redis.set(key, user.model_dump_json(), ex=GITHUB_CACHE_TTL)

    response.headers['X-Cache'] = 'MISS'
    return user
