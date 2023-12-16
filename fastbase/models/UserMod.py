from uuid import UUID
from datetime import datetime
from typing import Type, Self, Callable, Awaitable
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, String, JSON, Relationship, select, exists
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.exc import NoResultFound
from datetime import date
from pydantic import EmailStr
from icecream import ic

from .mixins import DTMixin, UuidPK, UpdatedAtMixin, IntPK
from ..utils import modstr
from ..exceptions import CallbackError



class ProfileMod(IntPK, UpdatedAtMixin, SQLModel):
    gender: str | None = Field(max_length=20, nullable=True)
    birthday: date | None = Field(nullable=True)
    meta: dict = Field(sa_column=Column(JSON), default={})

    def __repr__(self):
        return modstr(self)


class UserMod(DTMixin, UuidPK, SQLModel):
    email: str = Field(max_length=190, unique=True)
    username: str = Field(max_length=190, unique=True)
    display: str = Field(max_length=199)
    timezone: str | None = Field(max_length=190, default='+0000')
    role: str = Field(max_length=20, default='user')
    groups: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    permissions: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    # TODO: Optional verification
    is_verified: bool = Field(default=True)
    # TODO: Optional activation
    is_active: bool = Field(default=True)
    banned_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    def __repr__(self):
        return modstr(self, 'email')

    # TESTME: Untested
    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Type[Self]:
        """
        Get User by their email.
        :param session:     session
        :param email:       User email
        :return:            User
        :raises NoResultFound: User doesn't exist
        """
        stmt = select(cls).where(cls.email == email)
        execdata = await session.exec(stmt)
        data = execdata.one()
        return data

    # TESTME: Untested
    @classmethod
    async def get_by_id(cls, session: AsyncSession, uid: str) -> Type[Self]:
        """
        Get User by their id.
        :param session:     session
        :param uid:         User id
        :return:            User
        :raises NoResultFound: User doesn't exist
        """
        data = await session.get(cls, UUID(uid))
        return data

    # TESTME: Untested
    @classmethod
    async def exists(cls, session: AsyncSession, email: EmailStr) -> bool:
        """Check if a user exists"""
        stmt = select(cls.id).where(cls.email == email)
        execdata = await session.exec(stmt)
        if _ := execdata.first():
            return True

    # TESTME: Untested
    async def attach_group(self, session: AsyncSession, name: str,
                           *, caching: Callable[[str, list], None] | None = None,
                           async_callback: Callable[[str, list], Awaitable[None]] | None = None, ):
        """
        Add group to user. Removes duplicates.
        :param session:     AsyncSession
        :param name:        Group name
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :return:            None
        """
        # async with AsyncSession(async_engine) as sess: # noqa
        # async with asynccontextmanager(get_session)() as sess: # noqa
        #     user = await User.get_by_email(sess, 'admin@gmail.com', skip_cache=True)
        if name not in self.groups:
            groups = list({*self.groups, name})
            self.groups = groups
            await session.commit()

            if caching:
                caching(self.email, groups)
            if async_callback:
                await async_callback(self.email, groups)

            return groups

    # TESTME: Untested
    async def detach_group(self, session: AsyncSession, name: str,
                           *, caching: Callable[[str, list], None] | None = None,
                           async_callback: Callable[[str, list], Awaitable[None]] | None = None) -> set[str]:
        """
        Remove group from user.
        :param session:     AsyncSession
        :param name:        Group name
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :return:            None
        """
        if name in self.groups:
            groups = set(self.groups)
            groups.discard(name)
            self.groups = list(groups)
            await session.commit()

            if caching:
                caching(self.email, list(groups))
            if async_callback:
                await async_callback(self.email, list(groups))
            return groups
