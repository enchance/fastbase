from typing import Self
from sqlmodel import SQLModel, Field, String
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.exc import IntegrityError

from .mixins import IntPK, UpdatedAtMixin
from ..utils import modstr


class Role(IntPK, UpdatedAtMixin, SQLModel, table=True):
    __tablename__ = 'auth_role'
    name: str = Field(max_length=20, unique=True)
    description: str | None = Field(max_length=199, default='')
    groups: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])

    def __repr__(self):
        return modstr(self, 'name', 'description')

    # TESTME: Untested
    @classmethod
    async def create(cls, session: AsyncSession, *, name:str, groups: set, description: str | None = None) -> Self:
        """Create new role. Requires the role.create permission."""
        try:
            role = cls(name=name, groups=groups, description=description)
            session.add(role)
            await session.commit()
            await session.refresh(role)
            return role
        except IntegrityError:
            raise

    # TESTME: Untested
    @classmethod
    async def reset(cls, session: AsyncSession, id: int, groups: set) -> Self:
        """Reset groups. Requires role.reset permission."""
        if role := await session.get(cls, id):
            role.groups = groups
            session.add(role)
            await session.commit()
        return role

    # TESTME: Untested
    @classmethod
    async def describe(cls, session: AsyncSession, id: int, description: str) -> Self:
        """Change role description. Requires role.update permission."""
        if role := await session.get(cls, id):
            role.description = description
            session.add(role)
            await session.commit()
        return role
