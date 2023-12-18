from typing import Self
from sqlmodel.ext.asyncio.session import AsyncSession
from redis_om import NotFoundError

from fastbase.models import UserMod, ProfileMod, TaxonomyMod, OptionMod


class User(UserMod, table=True):
    __tablename__ = 'auth_user'

    # async def get_by_email(cls, session: AsyncSession, email: str, skip_cache: bool = True) -> Self:
    #     """Get User by email with redis."""
    #     try:
    #         if skip_cache:
    #             raise NotFoundError()
    #         user = cls.from_cache(email)
    #     except NotFoundError:       # redis error
    #         user = await cls._fetch(session, email=email)
    #         user.to_cache()
    #     return user


class Profile(ProfileMod, table=True):
    __tablename__ = 'auth_profile'


class Taxonomy(TaxonomyMod, table=True):
    __tablename__ = 'app_taxonomy'


class Option(OptionMod, table=True):
    __tablename__ = 'app_option'