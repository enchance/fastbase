from typing import Self
from sqlmodel import SQLModel, Field, String
from sqlalchemy import Column
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.exc import IntegrityError

from .mixins import IntPK
from ..utils import modstr
from fastbase import ic


class Group(IntPK, SQLModel, table=True):
    __tablename__ = 'auth_group'
    name: str = Field(max_length=20, unique=True)
    description: str = Field(max_length=199, default='')
    permissions: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])

    def __str__(self):
        return modstr(self, 'name')

    # TESTME: Untested
    @classmethod
    async def create(cls, session: AsyncSession, name: str,  permissions: set,
                     description: str | None = None) ->Self:
        """Create a new group"""
        try:
            group = cls(name=name, permissions=permissions, description=description)
            session.add(group)
            await session.commit()
            await session.refresh(group)
            return group
        except IntegrityError:
            raise

    # TESTME: Untested
    @classmethod
    async def append(cls, session: AsyncSession, *, id: int, permissions: set) -> Self:
        """Append new permissions to group"""
        if group := await session.get(cls, id):
            group.permissions = {*group.permissions, *permissions}
            session.add(group)
            await session.commit()
        return group