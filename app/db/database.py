from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pathlib import Path

from sqlalchemy.orm import DeclarativeBase

# Абсолютный путь к app/db.sqlite3 — не зависит от того, откуда запущено приложение/alembic
DB_PATH = Path(__file__).resolve().parent.parent.parent / 'db.sqlite3'
DATABASE_URL: str = f'sqlite+aiosqlite:///{DB_PATH}'


engine = create_async_engine(DATABASE_URL, echo=True) #echo=True - видим логи того что присходит


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    "Базовый класс для всех модлей"
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session

