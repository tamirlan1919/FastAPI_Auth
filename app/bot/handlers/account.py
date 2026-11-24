from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.db import get_linked_user
from app.db.database import async_session_maker
from app.repositories.post_repo import PostRepo
from app.repositories.user_repo import UserRepo

router = Router()


@router.message(Command('me'))
async def handle_me(message: Message):
    async with async_session_maker() as session:
        user = await get_linked_user(message, session)
        if user is None:
            return

    roles = ', '.join(user.roles) if user.roles else '—'
    await message.answer(
        f'👤 {html.bold(html.quote(user.username))}\n'
        f'Email: {html.quote(user.email)}\n'
        f'Роли: {html.quote(roles)}\n'
        f'Зарегистрирован: {user.created_at:%d.%m.%Y}'
    )


@router.message(Command('posts'))
async def handle_posts(message: Message):
    async with async_session_maker() as session:
        user = await get_linked_user(message, session)
        if user is None:
            return
        posts = await PostRepo(session).get_by_author(user.id)

    if not posts:
        await message.answer('У вас пока нет постов.')
        return

    lines = []
    for post in posts:
        tags = ' '.join(f'#{html.quote(tag.name)}' for tag in post.tags)
        lines.append(f'• {html.quote(post.title)} {tags}'.rstrip())
    await message.answer('📝 Ваши посты:\n' + '\n'.join(lines))


@router.message(Command('unlink'))
async def handle_unlink(message: Message):
    async with async_session_maker() as session:
        user = await get_linked_user(message, session)
        if user is None:
            return
        await UserRepo(session).set_telegram_id(user, None)

    await message.answer('Telegram отвязан от аккаунта. Чтобы привязать снова — получите новую ссылку в профиле.')
