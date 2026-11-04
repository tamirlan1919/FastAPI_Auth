from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.models import User, Profile
from app.shemas.user import RegisterWithProfile

class UserAlreadyExists(Exception):
    pass


async def register_with_profile(session: AsyncSession, data: RegisterWithProfile) -> User:
    async with session.begin():
        taken = await session.scalar(
            select(User.id).where(or_(User.username == data.username, User.email == data.email))
        )
        if taken is not None:
            raise UserAlreadyExists('Username or email already taken')

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            roles=['user']
        )
        session.add(user)
        await session.flush()

        if data.profile.city.lower() == 'атлантида':
            raise ValueError('Атлантида утонула- такого города нет')

        user.profile = Profile(
            bio=data.profile.bio,
            city=data.profile.city,
            country=data.profile.country
        )
        return user