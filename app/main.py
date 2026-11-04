from asyncio import ensure_future

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routers import users, auth, todos, stats, posts, reports
from app.db.database import Base, engine
from app.db import models  # noqa: F401 — регистрирует модели в Base.metadata для create_all
from contextlib import asynccontextmanager
from app.db.redis_db import create_redis
from app.broker.rabbit import connect_rabbit, declare_events_exchange, EventPublisher



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = create_redis()
    await app.state.redis.ping()

    app.state.rabbit = await connect_rabbit('auth-api')
    channel = await app.state.rabbit.channel()
    exchange = await declare_events_exchange(channel)
    app.state.publisher = EventPublisher(exchange)

    yield
    await app.state.rabbit.close()
    await app.state.redis.aclose()



app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(stats.router)
app.include_router(posts.router)
app.include_router(reports.router)

# Prometheus: middleware считает запросы/латентность, GET /metrics отдаёт их в формате Prometheus
Instrumentator(
    should_group_status_codes=False,         # status="404", а не "4xx"
    should_ignore_untemplated=True,          # не плодим метрики на несуществующие пути (сканеры, опечатки)
    should_instrument_requests_inprogress=True,
    inprogress_labels=True,
    excluded_handlers=["/metrics"],
).instrument(app).expose(app, include_in_schema=False)


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)