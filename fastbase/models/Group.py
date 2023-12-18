from typing import Self
from sqlmodel import SQLModel, Field, String, select
from sqlalchemy import Column
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.exc import IntegrityError

from .mixins import IntPK, UpdatedAtMixin
from ..utils import modstr
from ..schemas import *


class Group(IntPK, UpdatedAtMixin, SQLModel, table=True):
    __tablename__ = 'auth_group'
    name: str = Field(max_length=20, unique=True)
    description: str = Field(max_length=199, default='')
    permissions: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])

    def __repr__(self):
        return modstr(self, 'name')

    @classmethod
    async def create(cls, session: AsyncSession, *,
                     name: str,  permissions: set | None = None,
                     description: str | None = None) -> Self:
        """Create a new group. Requires group.create permission."""
        try:
            group = cls(name=name, permissions=permissions, description=description)
            session.add(group)
            await session.commit()
            await session.refresh(group)
            return group
        except IntegrityError:
            raise

    # PLACEHOLDER: To follow
    @classmethod
    async def delete(cls, name: str):
        """Delete a group. Updates cache."""
        pass

    async def add_all(self, session: AsyncSession, permissions: set[str]):
        """Append new permissions to group. Requires group.update permission."""
        self.permissions = {*self.permissions, *permissions}                # noqa
        session.add(self)
        await session.commit()

    async def reset(self, session: AsyncSession, permissions: set[str] | None = None):
        """Reset permissions. Requires group.reset permission."""
        self.permissions = permissions or []
        session.add(self)
        await session.commit()

    async def describe(self, session: AsyncSession, description: str | None = None):
        """Change group description. Requires group.update permission."""
        self.description = description or ''
        await session.commit()

    # TESTME: Untested
    @classmethod
    async def collate(cls, session: AsyncSession, nameset: set[str]) -> set[str]:
        stmt = select(cls.permissions).where(cls.name.in_(nameset))
        edata = await session.exec(stmt)
        alldata = edata.all()

        ss = set()
        for i in alldata:
            ss.update(i)
        return ss
