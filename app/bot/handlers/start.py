from aiogram import Router, html
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from redis.asyncio import Redis

from app.bot.links import link_key
from app.db.database import async_session_maker
from app.repositories.user_repo import UserRepo

router = Router()


@router.message(CommandStart(deep_link=True))
async def handle_start_link(message: Message, command: CommandObject, redis: Redis):
    # getdel — код одноразовый: повторный переход по той же ссылке уже ничего не найдёт
    user_id = await redis.getdel(link_key(command.args))
    if user_id is None:
        await message.answer('Ссылка устарела или уже использована. Получите новую в профиле.')
        return

    async with async_session_maker() as session:
        user_repo = UserRepo(session)

        already = await user_repo.get_by_telegram_id(message.from_user.id)
        if already is not None:
            if already.id == int(user_id):
                await message.answer('Этот Telegram уже привязан к вашему аккаунту.')
            else:
                await message.answer('Этот Telegram уже привязан к другому аккаунту. Сначала отвяжите его: /unlink')
            return

        target = await user_repo.get_by_id(int(user_id))
        if target is None:
            await message.answer('Аккаунт не найден.')
            return

        await user_repo.set_telegram_id(target, message.from_user.id)

    await message.answer(
        f'Готово! Telegram привязан к аккаунту {html.bold(html.quote(target.username))}.\n'
        f'Попробуйте /me и /posts'
    )


# Обычный /start без кода — регистрируется после deep-link хендлера, поэтому ловит только его
@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        'Привет! Я бот auth-api.\n'
        'Чтобы привязать аккаунт, получите ссылку в профиле (POST /telegram/link) и откройте её.'
    )
