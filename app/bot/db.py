from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.repositories.user_repo import UserRepo


NOT_LINKED = 'Аккаунт не привязан. Получите ссылку в профиле auth-api и откройте её.'


async def get_linked_user(message: Message, session: AsyncSession) -> User | None:
    user = await UserRepo(session).get_by_telegram_id(message.from_user.id)
    if user is None:
        await message.answer(NOT_LINKED)
    return user
