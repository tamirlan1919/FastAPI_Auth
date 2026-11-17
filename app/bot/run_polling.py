import asyncio
import logging

from app.bot.setup import BOT_COMMANDS, create_dispatcher, create_bot
from app.core.config import settings
from app.db.database import engine
from app.db.redis_db import create_redis


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    engine.echo = False

    if settings.telegram_bot_token is None:
        raise SystemExit("Please set a telegram bot token")

    redis = create_redis()
    bot = create_bot(settings.telegram_bot_token.get_secret_value(), settings.telegram_api_url)
    dp = create_dispatcher(redis=redis)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=BOT_COMMANDS)
        # start_polling сам закроет сессию бота при остановке (close_bot_session=True)
        await dp.start_polling(bot)
    finally:
        await redis.aclose()


if __name__ == '__main__':
    asyncio.run(main())
