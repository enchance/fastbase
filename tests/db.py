from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from redis_om.connections import get_redis_connection
from decouple import config



DATABASE_TEST_URL = config('TEST_PG_URL')
REDIS_TEST_URL = config('TEST_REDIS_URL')

async_engine = create_async_engine(DATABASE_TEST_URL, echo=True)
redis = get_redis_connection(url=REDIS_TEST_URL)
async_session = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)   # noqa