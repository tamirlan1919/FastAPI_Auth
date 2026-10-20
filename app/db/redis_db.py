from fastapi import Request
from redis.asyncio import Redis

from app.core.config import settings


def create_redis() -> Redis:
    return Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,

    )


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
