import itertools
from typing import Self
from sqlmodel import SQLModel, Field, String, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.exc import IntegrityError

from .mixins import IntPK, UpdatedAtMixin
from ..utils import modstr
from .Group import Group


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


class RoleService:
    @classmethod
    async def fetch_group_names(cls, session: AsyncSession, role: str) -> set[str]:
        stmt = select(Role.groups).where(Role.name == role)
        execdata = await session.exec(stmt)
        ll = execdata.one()
        return set(ll)


class PermissionService:
    @classmethod
    async def fetch_permissions(cls, session: AsyncSession, groups: set[str]) -> set[str]:
        stmt = select(Group.permissions).where(Group.name.in_(groups))
        execdata = await session.exec(stmt)
        datalist = execdata.all()
        datalist = set(itertools.chain.from_iterable(datalist))
        return datalist
