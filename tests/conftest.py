import pytest, asyncio, httpx, pytest_asyncio
from typing import Generator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from .testapp.main import app, silent_engine
from .seed import seed_groups, seed_roles



@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """
    DO NOT DELETE (even if not in use):
    This overwrites the default scope of the event_loop from fn to session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(app=app, base_url='http://test/') as client:
        yield client


@pytest_asyncio.fixture(scope='module')
async def session() -> AsyncSession:
    async_session = sessionmaker(bind=silent_engine, autoflush=False, expire_on_commit=False,
                                 class_=AsyncSession)

    async with async_session() as session:
        async with silent_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        await seed(session)
        yield session

    async with silent_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await silent_engine.dispose()


async def seed(session: AsyncSession):
    await seed_groups(session)
    await seed_roles(session)
    # await seed_accounts(session)