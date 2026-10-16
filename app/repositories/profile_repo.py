from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Profile


class ProfileRepo():

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(self, user_id: int) -> Profile | None:
        stmt = (
            select(Profile)
            .where(Profile.user_id == user_id)
            .options(selectinload(Profile.user))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_id: int, bio: str, city: str, country: str) -> Profile:
        # user_id уникален — у пользователя может быть только один профиль (1 к 1)
        profile = Profile(user_id=user_id, bio=bio, city=city, country=country)
        self.session.add(profile)
        await self.session.commit()
        return await self.get_by_user_id(user_id)

    async def update(self, user_id: int, bio: str | None = None,
                     city: str | None = None, country: str | None = None) -> Profile | None:
        profile = await self.get_by_user_id(user_id)
        if profile is None:
            return None
        if bio is not None:
            profile.bio = bio
        if city is not None:
            profile.city = city
        if country is not None:
            profile.country = country
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def delete(self, user_id: int):
        profile = await self.get_by_user_id(user_id)
        if profile:
            await self.session.delete(profile)
            await self.session.commit()
            return True
        return False
