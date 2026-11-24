from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from redis.asyncio import Redis
from app.bot.handlers import router


def create_bot(token: str, api_url: str = 'https://api.telegram.org') -> Bot:
    session = AiohttpSession(api=TelegramAPIServer.from_base(api_url))
    return Bot(token=token, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def create_dispatcher(redis: Redis) -> Dispatcher:
    # kwargs Dispatcher'а попадают в workflow_data — так redis приходит аргументом в хендлеры
    dp = Dispatcher(redis=redis)
    dp.include_router(router)
    return dp

BOT_COMMANDS = [
    BotCommand(command='me', description='Мой профиль в auth-api'),
    BotCommand(command='posts', description='Мои посты'),
    BotCommand(command='unlink', description='Отвязать Telegram'),
]

