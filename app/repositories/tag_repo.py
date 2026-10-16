from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Post, Tag


class TagRepo():

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, name: str) -> Tag | None:
        stmt = select(Tag).where(Tag.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_tags(self):
        stmt = select(Tag).order_by(Tag.name)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_with_posts(self, name: str) -> Tag | None:
        # В async-режиме ленивая загрузка не работает, поэтому связи грузим явно
        stmt = (
            select(Tag)
            .where(Tag.name == name)
            .options(selectinload(Tag.posts).selectinload(Post.author))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create_many(self, names: list[str]) -> list[Tag]:
        """Возвращает теги по именам, недостающие создает. Не коммитит — это делает вызывающий."""
        names = list(dict.fromkeys(n.strip() for n in names if n.strip()))
        if not names:
            return []

        stmt = select(Tag).where(Tag.name.in_(names))
        result = await self.session.execute(stmt)
        existing = {tag.name: tag for tag in result.scalars().all()}

        for name in names:
            if name not in existing:
                tag = Tag(name=name)
                self.session.add(tag)
                existing[name] = tag

        await self.session.flush()
        return [existing[name] for name in names]

    async def create(self, name: str) -> Tag:
        tag = Tag(name=name)
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def delete(self, name: str):
        tag = await self.get_by_name(name)
        if tag:
            await self.session.delete(tag)
            await self.session.commit()
            return True
        return False
