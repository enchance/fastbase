import pytest, asyncio, httpx, pytest_asyncio
from typing import Generator, Callable
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from tests.db import async_engine, redis
from tests.seed import seed_accounts
from tests.models import *



@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """
    DO NOT DELETE:
    This overwrites the default scope of the event_loop from fn to session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# @pytest_asyncio.fixture
# async def client():
#     async with httpx.AsyncClient(app=app, base_url='http://test/') as client:
#         yield client


@pytest_asyncio.fixture(scope='session')
async def session() -> AsyncSession:
    # ic('SESSION')
    async_session = sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        await seed(session)
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        redis.flushdb()

    await async_engine.dispose()


async def seed(session: AsyncSession):
    # ic('SEEDING')
    # await seed_groups(session)
    # await seed_roles(session)
    await seed_accounts(session, False)


@pytest_asyncio.fixture(scope='module')
async def user(session) -> User:
    user = User()
    # user = await User.get_by_email(session, VERIFIED_EMAIL)
    return user