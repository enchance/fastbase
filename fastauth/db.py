from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from decouple import config


DATABASE_URL = config('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session