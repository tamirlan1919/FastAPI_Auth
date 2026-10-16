from app.db.models import Post, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class UserRepo():

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_users(self):
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_with_profile(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(User.username == username)
            .options(selectinload(User.profile))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_posts(self, username: str) -> User | None:
        # Посты пользователя вместе с их тегами
        stmt = (
            select(User)
            .where(User.username == username)
            .options(selectinload(User.posts).selectinload(Post.tags))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_full(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(User.username == username)
            .options(
                selectinload(User.profile),
                selectinload(User.posts).selectinload(Post.tags),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def create(self, username: str, email: str, hashed_password: str,
                    roles: list[str]) -> User:
        user = User(username=username, email=email, hashed_password=hashed_password, roles=roles)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, username: str, email: str):
        user = await self.get_by_username(username)
        if user:
            user.email = email
            user.username = username
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None

    async def delete(self, username: str):
        user = await self.get_by_username(username)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False





