import asyncio
import random

from sqlalchemy import select

from app.core.security import hash_password
from app.db.database import async_session_maker
from app.db.models import User, Post, Tag

TITLES = ['Как я перестал бояться и полюбил', '10 фактов, которые вы не знали про', 'Почему все так любят',
          'Боль и страдания:', 'Шпаргалка по', 'Мой первый опыт с']
TAG_NAMES = ['python', 'fastapi', 'sql', 'redis', 'mongo', 'asyncio']
AUTHORS = 30
POSTS = 300


async def main():
    random.seed(42)
    async with async_session_maker() as session:
        async with session.begin():
            already = await session.scalar(select(User.id).where(User.username == 'seed_user_01'))
            if already:
                print('Данные уже есть - пропускаем')
                return

            password = hash_password('Seed-pass123')
            authors = [
                User(
                    username=f'seed_user_{i:02}',
                    email=f'seed_user_{i:02}@example.com',
                    hashed_password=password,
                    roles=['user'],
                )
                for i in range(1, AUTHORS + 1)
            ]
            session.add_all(authors)

            # Теги уникальны по name — берём существующие, недостающие создаём
            existing = await session.scalars(select(Tag).where(Tag.name.in_(TAG_NAMES)))
            tags = {tag.name: tag for tag in existing}
            for name in TAG_NAMES:
                if name not in tags:
                    tags[name] = Tag(name=name)
                    session.add(tags[name])
            tag_list = list(tags.values())

            posts = []
            for _ in range(POSTS):
                post_tags = random.sample(tag_list, k=random.randint(1, 3))
                posts.append(Post(
                    title=f'{random.choice(TITLES)} {post_tags[0].name}',
                    author=random.choice(authors),
                    tags=post_tags,
                ))
            session.add_all(posts)

        print(f'Создано: {AUTHORS} авторов, {POSTS} постов, {len(tag_list)} тегов')


if __name__ == '__main__':
    asyncio.run(main())
