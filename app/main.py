import logging
from asyncio import ensure_future

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routers import users, auth, todos, stats, posts, reports, github, weather, yandex_auth, telegram
from app.bot.setup import create_bot, create_dispatcher, BOT_COMMANDS
from app.clients.yandex_oauth import YandexOauthClient
from app.core.config import settings
from app.core.error_handler import install_error_handler
from app.core.request_id import request_id_middleware
from app.db.database import Base, engine
from app.db import models  # noqa: F401 — регистрирует модели в Base.metadata для create_all
from contextlib import asynccontextmanager
from app.db.redis_db import create_redis
from app.broker.rabbit import connect_rabbit, declare_events_exchange, EventPublisher


logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # SQL-запросы в лог (один раз, без echo=True)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = create_redis()
    app.state.rabbit = None
    app.state.yandex_oauth = app.state.yandex_disk = None
    app.state.bot = app.state.dp = None

    # try/finally: если старт упадёт на середине, уже открытые соединения всё равно закроются
    try:
        await app.state.redis.ping()

        app.state.rabbit = await connect_rabbit('auth-api')
        channel = await app.state.rabbit.channel()
        exchange = await declare_events_exchange(channel)
        app.state.publisher = EventPublisher(exchange)

        if settings.yandex_client_id and settings.yandex_client_secret:
            app.state.yandex_oauth = YandexOauthClient(
                client_id=settings.yandex_client_id,
                client_secret=settings.yandex_client_secret.get_secret_value(),
                redirect_uri=settings.yandex_redirect_uri,
                oauth_url=settings.yandex_oauth_url,
                login_url=settings.yandex_login_url,
            )

        if settings.telegram_bot_token:
            bot = create_bot(settings.telegram_bot_token.get_secret_value(), settings.telegram_api_url)
            dp = create_dispatcher(redis=app.state.redis)
            app.state.bot = bot
            app.state.dp = dp
            await bot.set_my_commands(BOT_COMMANDS)
            if settings.telegram_webhook_base:
                webhook_base = settings.telegram_webhook_base.rstrip('/')
                if not webhook_base.startswith('https://'):
                    raise RuntimeError(
                        'TELEGRAM_WEBHOOK_BASE должен быть публичным https-адресом (например, от ngrok). '
                        'Для локальной разработки уберите его из .env и запустите бота через polling: '
                        'python -m app.bot.run_polling'
                    )
                if settings.telegram_webhook_secret is None:
                    raise RuntimeError('TELEGRAM_WEBHOOK_SECRET не задан')
                await bot.set_webhook(
                    url=f'{webhook_base}/telegram/webhook',
                    secret_token=settings.telegram_webhook_secret.get_secret_value(),
                    allowed_updates=dp.resolve_used_update_types(),
                )
                logger.info('telegram webhook set')

        yield
    finally:
        # bot.close() — это метод Telegram API (выход с сервера), а не закрытие соединения
        if app.state.bot is not None:
            await app.state.bot.session.close()
        if app.state.rabbit is not None:
            await app.state.rabbit.close()
        await app.state.redis.aclose()
        for client in (app.state.yandex_oauth, app.state.yandex_disk):
            if client is not None:
                await client.aclose()




app = FastAPI(lifespan=lifespan)
install_error_handler(app=app)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(stats.router)
app.include_router(posts.router)
app.include_router(reports.router)
app.include_router(github.router)
app.include_router(weather.router)
app.include_router(yandex_auth.router)
app.include_router(telegram.router)
app.middleware('http')(request_id_middleware)


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