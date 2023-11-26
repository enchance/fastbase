from uuid import UUID
from typing import Type, Self
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, String, JSON, Relationship, select, exists
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.exc import NoResultFound
from datetime import date
from pydantic import EmailStr
from icecream import ic

from .mixins import DTMixin, UuidPK
from ..utils import modstr


USER_TABLE = 'auth_user'
USER_PK = f'{USER_TABLE}.id'
author_fk = Field(foreign_key=USER_PK)
author_fk_nullable = Field(foreign_key=USER_PK, nullable=True)



class UserMod(DTMixin, UuidPK, SQLModel):
    __tablename__ = USER_TABLE
    username: str = Field(max_length=190, unique=True)
    email: str = Field(max_length=190, unique=True)
    display: str | None = Field(max_length=199, nullable=True)
    groups: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    permissions: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    gender: str | None = Field(max_length=20, nullable=True)
    timezone: str | None = Field(max_length=190, default='+0000')
    meta: dict = Field(sa_column=Column(JSON), default={})

    def __str__(self):
        return modstr(self, 'username', 'email')

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: EmailStr) -> Type[Self] | None:
        """Get User by their email."""
        try:
            stmt = select(cls).where(cls.email == email)
            execdata = await session.exec(stmt)
            data = execdata.one()
            return data
        except NoResultFound:
            return

    @classmethod
    async def get_by_id(cls, session: AsyncSession, uid: str) -> Type[Self] | None:
        """Get User by their id."""
        try:
            data = await session.get(cls, UUID(uid))
            return data
        except NoResultFound:
            return

    @classmethod
    async def exists(cls, session: AsyncSession, email: EmailStr) -> bool:
        """Check if a user exists"""
        try:
            stmt = select(cls.id).where(cls.email == email)
            execdata = await session.exec(stmt)
            if _ := execdata.first():
                return True
            raise NoResultFound
        except NoResultFound:
            return False
