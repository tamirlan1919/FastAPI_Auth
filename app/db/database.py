from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL: str = 'sqlite+aiosqlite:///db.sqlite3'


engine = create_async_engine(DATABASE_URL, echo=True) #echo=True - видим логи того что присходит


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    "Базовый класс для всех модлей"
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session

