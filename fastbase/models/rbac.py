import itertools
from typing import Self
from sqlmodel import SQLModel, Field, String, select
from sqlalchemy import Column
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.exc import IntegrityError

from .mixins import IntPK, UpdatedAtMixin
from ..utils import modstr


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
        stmt = select(cls.permissions).where(cls.name.in_(nameset))     # noqa
        edata = await session.exec(stmt)
        alldata = edata.all()

        ss = set()
        for i in alldata:
            ss.update(i)
        return ss


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
