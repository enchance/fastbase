import uuid, secrets, time, arrow       # noqa
from random import choices
from typing import Annotated, TYPE_CHECKING
from faker import Faker
from decouple import config
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from fastapi import Depends
from icecream import ic
from fastbase import Fastbase, utils
from redis_om import NotFoundError

# from coreapp import settings as s
# from coreapp.auth import User, Group, Role, GroupRedis, RoleRedis
from .data import *
from tests.models import *



faker = Faker(['en', 'ja', 'fi'])
author_uuid: uuid.UUID


async def seed_accounts(session: AsyncSession, dummy_accounts: bool = True) -> list[str]:
    """Create nenw accounts for testing"""
    # ic('SEEDING_USERS')
    total = 0

    stmt = select(User.email)
    execdata = await session.exec(stmt)
    userlist = execdata.all()

    # # Super user
    # try:
    #     stmt = select(User).where(User.email == SUPER_EMAIL)
    #     execdata = await session.exec(stmt)
    #     super_user = execdata.one()
    #     author_uuid = super_user.id     # noqa
    # except NoResultFound:
    #     username, *_ = SUPER_EMAIL.partition('@')
    #     super_user = await User.create(session, email=SUPER_EMAIL, username=username, role='super')
    #     super_user.to_cache()
    #     author_uuid = super_user.id     # noqa
    #     total += 1

    # # Admin
    # if ADMIN_EMAIL not in userlist:
    #     username, *_ = ADMIN_EMAIL.partition('@')
    #     user = await User.create(session, username=username, email=ADMIN_EMAIL, role='admin')
    #     user.to_cache()
    #     total += 1
    #
    # # Verified
    # if VERIFIED_EMAIL not in userlist:
    #     username, *_ = VERIFIED_EMAIL.partition('@')
    #     user = await User.create(session, username=username, email=VERIFIED_EMAIL, role='user')
    #     user.to_cache()
    #     total += 1

    # # Unverified
    # if UNVERIFIED_EMAIL not in userlist:
    #     username, *_ = UNVERIFIED_EMAIL.partition('@')
    #     user = await User.create(session, username=username, email=UNVERIFIED_EMAIL, role='user')
    #     user.to_cache()
    #     total += 1
    #
    # # Banned
    # if BANNED_EMAIL not in userlist:    # noqa
    #     username, *_ = BANNED_EMAIL.partition('@')
    #     now = arrow.utcnow().datetime
    #     user = await User.create(session, username=username, email=BANNED_EMAIL, role='user', banned_at=now)
    #     user.to_cache()
    #     total += 1
    #
    # # Inactive
    # if INACTIVE_EMAIL not in userlist:
    #     username, *_ = INACTIVE_EMAIL.partition('@')
    #     user = await User.create(session, username=username, email=INACTIVE_EMAIL, role='user', is_active=False)
    #     user.to_cache()
    #     total += 1
    #
    # # Deleted
    # if DELETED_EMAIL not in userlist:   # noqa
    #     username, *_ = DELETED_EMAIL.partition('@')
    #     now = arrow.utcnow().datetime
    #     user = await User.create(session, username=username, email=DELETED_EMAIL, role='user', deleted_at=now)
    #     user.to_cache()
    #     total += 1
    #
    # # Custom group
    # if CUSTOM_GROUP_EMAIL not in userlist:
    #     username, *_ = CUSTOM_GROUP_EMAIL.partition('@')
    #     user = await User.create(session, username=username, email=CUSTOM_GROUP_EMAIL, role='user',
    #                              groups={GroupEnum.message, GroupEnum.empty, f'-{GroupEnum.upload.name}'})
    #     user.to_cache()
    #     total += 1
    #
    # # Custom permissions
    # if CUSTOM_PERMISSIONS_EMAIL not in userlist:
    #     username, *_ = CUSTOM_PERMISSIONS_EMAIL.partition('@')
    #     user = await User.create(session, username=username, email=CUSTOM_PERMISSIONS_EMAIL, role='user',
    #                              permissions={'message.read', '-settings.read'})
    #     user.to_cache()
    #     total += 1
    #
    # # Mock users
    # if dummy_accounts:
    #     for i in range(5):
    #         now = arrow.utcnow().datetime
    #         banned = now if choices([True, False], weights=(0.1, 0.9), k=1)[0] else None
    #         deleted = now if choices([True, False], weights=(0.1, 0.9), k=1)[0] else None
    #         role = choices(['super', 'admin', 'user'], weights=(0.15, 0.15, 0.7), k=1)[0]
    #
    #         data = faker.profile()
    #         email = data.get('mail')
    #         firstname, lastname = utils.split_fullname(data.get('name'))
    #         username = data.get('username')
    #         display = firstname
    #         user = await User.create(session, email=email, firstname=firstname, lastname=lastname, username=username,
    #                                  display=display, role=role, deleted_at=deleted, banned_at=banned)
    #         user.to_cache()
    #         total += 1

    return [f'ACCOUNTS_CREATED - {total} users']