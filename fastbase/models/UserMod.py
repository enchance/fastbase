from uuid import UUID
from typing import Type, Self
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, String, JSON, Relationship, select, exists
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.exc import NoResultFound
from datetime import date
from pydantic import EmailStr
from icecream import ic

from .mixins import DTMixin, UuidPK, UpdatedAtMixin
from ..utils import modstr



class ProfileMod(UpdatedAtMixin, SQLModel):
    gender: str | None = Field(max_length=20, nullable=True)
    birthday: date | None = Field(nullable=True)
    meta: dict = Field(sa_column=Column(JSON), default={})

    def __repr__(self):
        return modstr(self)


class UserMod(DTMixin, UuidPK, SQLModel):
    email: str = Field(max_length=190, unique=True)
    display: str = Field(max_length=199)
    timezone: str | None = Field(max_length=190, default='+0000')
    role: str = Field(max_length=20, default='user')
    groups: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    permissions: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    is_verified: bool = Field(default=True)
    is_active: bool = Field(default=True)
    is_banned: bool = Field(default=False)

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

    # PLACEHOLDER: To follow
    async def has(self, action: str) -> bool:
        pass

    # PLACEHOLDER: To follow
    async def has_group(self, name: str) -> bool:
        pass