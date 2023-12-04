from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastbase.models import Group, Role

from .data import *
from .testapp import *



async def seed_groups(session: AsyncSession) -> list[str]:
    # ic('SEEDING_GROUPS')
    total = 0
    fixturemap = GROUP_FIXTURES_DEV

    stmt = select(Group.name)
    execdata = await session.exec(stmt)
    groupnames = execdata.all()

    ll = []
    for name, datamap in fixturemap.items():
        if name in groupnames:
            continue

        permset = set()
        try:
            desc = datamap.pop('description')
        except KeyError:
            desc = ''
        if datamap:
            for title, perms in datamap.items():
                for i in perms:
                    permset.add(f'{title}.{i}')

        ll.append(Group(name=name, permissions=list(permset), description=desc))
        total += 1

        if ll:
            session.add_all(ll)
            await session.commit()

        # TODO: cache
    #         # Cache
    #         cachekey = s.redis.GROUP_PERMISSIONS.format(name)
    #         red.set(cachekey, permset)
    #         nameset.add(name)
    #     ll and await Group.bulk_create(ll)
    #
    #     # redis
    #     cachekey = s.redis.GROUPS
    #     nameset and red.set(cachekey, nameset)

    return [f'GROUPS_CREATED - {total} groups']


async def seed_roles(session: AsyncSession) -> list[str]:
    # ic('SEEDING_ROLES')
    total = 0
    fixturemap = {**ROLE_FIXTURES}

    stmt = select(Role.name)
    execdata = await session.exec(stmt)
    rolenames = execdata.all()

    ll = []
    for name, groups in fixturemap.items():     # noqa
        if name in rolenames:
            continue
        ll.append(Role(name=name, groups=groups))
        total += 1

    if ll:
        session.add_all(ll)
        await session.commit()

    return [f'ROLES_CREATED - {total} roles']