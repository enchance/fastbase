import arrow
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
from fastbase.exceptions import PermissionsException

from .mixins import DTMixin, UuidPK, UpdatedAtMixin, IntPK
from .Role import Role
from ..utils import modstr
from ..exceptions import CallbackError



class ProfileMod(IntPK, UpdatedAtMixin, SQLModel):
    gender: str | None = Field(max_length=20, nullable=True)
    birthday: date | None = Field(nullable=True)

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

    is_verified: bool = Field(default=True)                     # TODO: Optional verification
    is_active: bool = Field(default=True)                       # TODO: Optional activation
    banned_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True, index=True))

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

    async def has(self, data: str) -> bool:
        raise NotImplementedError()

    async def attach_group(self, session: AsyncSession, recipient: Self, name: str,
                           *, caching: Callable[[str, list], None] | None = None,
                           async_callback: Callable[[str, list], Awaitable[None]] | None = None):
        """
        Attach a group to user. Prevents duplicates.
        :param session:     AsyncSession
        :param recipient:   The user to recieve the group
        :param name:        Group name
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :raises PermissionsException:
        :return:            None
        """
        # async with AsyncSession(async_engine) as sess:
        # async with asynccontextmanager(get_session)() as sess:
        #     user = await User.get_by_email(sess, 'admin@gmail.com', skip_cache=True)
        def _attach(name_: str) -> list[str]:
            neg_ = f'-{name_}'
            groups_ = set(recipient.groups)

            if neg_ in groups_:
                groups_.remove(neg_)
            elif name_ not in groups_:
                groups_.add(name_)
            return list(groups_)

        if not await self.has('group.attach'):
            raise PermissionsException()

        if not name.strip() or self.email == recipient.email:
            return

        groups = _attach(name)
        recipient.groups = groups
        await session.commit()

        if caching:
            caching(recipient.email, groups)
        if async_callback:
            await async_callback(recipient.email, groups)

    async def detach_group(self, session: AsyncSession, recipient: Self, name: str,
                           *, caching: Callable[[str, list], None] | None = None,
                           async_callback: Callable[[str, list], Awaitable[None]] | None = None):
        """
        Remove a group from user. If the group is a starter group (can't be removed) then a negation is added.
        :param session:     AsyncSession
        :param recipient:   The user who's group is to be removed
        :param name:        Group name
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :raises PermissionsException:
        :return:            None
        """
        def _detach(name_: str) -> list[str]:
            neg_ = f'-{name_}'
            groups_ = set(recipient.groups)

            if name_ in groups_:
                groups_.remove(name_)
            else:
                groups_.add(neg_)
            return list(groups_)

        if not await self.has('group.detach'):
            raise PermissionsException()

        if not name.strip() or self.email == recipient.email:
            return

        groups = _detach(name)
        recipient.groups = groups
        await session.commit()

        if caching:
            caching(recipient.email, list(groups))
        if async_callback:
            await async_callback(recipient.email, list(groups))

    async def attach_permission(self, session: AsyncSession, recipient: Self, perm: str,
                                *, caching: Callable[[str, list], None] | None = None,
                                async_callback: Callable[[str, list], Awaitable[None]] | None = None):
        """
        Attach a permission to user. Prevents duplicates.
        :param session:     AsyncSession
        :param recipient:   The user to recieve the group
        :param perm:        Permission
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :raises PermissionsException:
        :return:            None
        """
        # async with AsyncSession(async_engine) as sess:
        # async with asynccontextmanager(get_session)() as sess:
        #     user = await User.get_by_email(sess, 'admin@gmail.com', skip_cache=True)
        def _attach(name_: str) -> list[str]:
            neg_ = f'-{name_}'
            perms_ = set(recipient.permissions)

            if neg_ in perms_:
                perms_.remove(neg_)
            elif name_ not in perms_:
                perms_.add(name_)
            return list(perms_)

        if not await self.has('permission.attach'):
            raise PermissionsException()

        if not perm.strip() or self.email == recipient.email:
            return

        permissions = _attach(perm)
        recipient.permissions = permissions
        await session.commit()

        if caching:
            caching(recipient.email, permissions)
        if async_callback:
            await async_callback(recipient.email, permissions)

    async def detach_permission(self, session: AsyncSession, recipient: Self, perm: str,
                                *, caching: Callable[[str, list], None] | None = None,
                                async_callback: Callable[[str, list], Awaitable[None]] | None = None):
        """
        Remove a permission from user. If the permission is a starter group (can't be removed) then a negation is added.
        :param session:     AsyncSession
        :param recipient:   The user who's group is to be removed
        :param perm:        Permission
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :raises PermissionsException:
        :return:            None
        """
        def _detach(perm_: str) -> list[str]:
            neg_ = f'-{perm_}'
            perms_ = set(recipient.permissions)

            if perm_ in perms_:
                perms_.remove(perm_)
            else:
                perms_.add(neg_)
            return list(perms_)

        if not await self.has('permission.detach'):
            raise PermissionsException()

        if not perm.strip() or self.email == recipient.email:
            return

        permissions = _detach(perm)
        recipient.permissions = permissions
        await session.commit()

        if caching:
            caching(recipient.email, list(permissions))
        if async_callback:
            await async_callback(recipient.email, list(permissions))

    # TESTME: Untested
    async def ban(self, session: AsyncSession, recipient: Self,
                  *, caching: Callable[[str, datetime], None] | None = None,
                  async_callback: Callable[[str, datetime], Awaitable[None]] | None = None):
        """
        Ban user.
        :param session:     AsyncSession
        :param recipient:   The user to ban
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :raises PermissionsException:
        :return:            None
        """
        if not await self.has('ban.attach'):
            raise PermissionsException()

        if recipient.banned_at is not None or self.email == recipient.email:
            return

        now = arrow.utcnow().datetime
        recipient.banned_at = now
        await session.commit()

        if caching:
            caching(recipient.email, now)
        if async_callback:
            await async_callback(recipient.email, now)

    # TESTME: Untested
    async def unban(self, session: AsyncSession, recipient: Self,
                    *, caching: Callable[[str, None], None] | None = None,
                    async_callback: Callable[[str, None], Awaitable[None]] | None = None):
        """
        Unban user.
        :param session:     AsyncSession
        :param recipient:   The user to unban
        :param caching:     Callback for caching data
        :param async_callback:    Async callback for generic use
        :raises PermissionsException:
        :return:            None
        """
        if not await self.has('ban.detach'):
            raise PermissionsException()

        if recipient.banned_at is None or self.email == recipient.email:
            return

        recipient.banned_at = None
        await session.commit()

        if caching:
            caching(recipient.email, None)
        if async_callback:
            await async_callback(recipient.email, None)