from fastapi import APIRouter

from app.api.deps import RedisDep

router = APIRouter(prefix="/stats", tags=["Статистика Redis"])

@router.get("/ping")
async def ping(redis: RedisDep):
    return {'redis': await redis.ping()}


@router.post('/visits')
async def add_visit(redis: RedisDep):
    total = await redis.incr('stats:visits')
    return {'total': total}


@router.get('/visits')
async def get_visits(redis: RedisDep):
    value = await redis.get('stats:visits')
    return {'value': value}