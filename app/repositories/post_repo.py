from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Post, Tag
from app.repositories.tag_repo import TagRepo


class PostRepo():

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.tag_repo = TagRepo(session)

    def _with_relations(self):
        # Сразу подгружаем автора и теги, чтобы post.author / post.tags были доступны вне сессии
        return select(Post).options(selectinload(Post.author), selectinload(Post.tags))

    async def get_by_id(self, post_id: int) -> Post | None:
        stmt = self._with_relations().where(Post.id == post_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_posts(self):
        stmt = self._with_relations().order_by(Post.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_author(self, author_id: int):
        stmt = self._with_relations().where(Post.author_id == author_id).order_by(Post.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_tag(self, tag_name: str):
        # JOIN через ассоциативную таблицу post_tags
        stmt = (
            self._with_relations()
            .join(Post.tags)
            .where(Tag.name == tag_name)
            .order_by(Post.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, title: str, author_id: int, tag_names: list[str] | None = None) -> Post:
        tags = await self.tag_repo.get_or_create_many(tag_names or [])
        post = Post(title=title, author_id=author_id, tags=tags)
        self.session.add(post)
        await self.session.commit()
        return await self.get_by_id(post.id)

    async def update(self, post_id: int, title: str | None = None,
                     tag_names: list[str] | None = None) -> Post | None:
        """tag_names=None — теги не трогаем, [] — убираем все теги."""
        post = await self.get_by_id(post_id)
        if post is None:
            return None
        if title is not None:
            post.title = title
        if tag_names is not None:
            post.tags = await self.tag_repo.get_or_create_many(tag_names)
        await self.session.commit()
        return await self.get_by_id(post_id)

    async def add_tags(self, post_id: int, tag_names: list[str]) -> Post | None:
        post = await self.get_by_id(post_id)
        if post is None:
            return None
        for tag in await self.tag_repo.get_or_create_many(tag_names):
            if tag not in post.tags:
                post.tags.append(tag)
        await self.session.commit()
        return await self.get_by_id(post_id)

    async def remove_tag(self, post_id: int, tag_name: str) -> Post | None:
        post = await self.get_by_id(post_id)
        if post is None:
            return None
        post.tags = [tag for tag in post.tags if tag.name != tag_name]
        await self.session.commit()
        return await self.get_by_id(post_id)

    async def delete(self, post_id: int):
        post = await self.get_by_id(post_id)
        if post:
            await self.session.delete(post)
            await self.session.commit()
            return True
        return False
