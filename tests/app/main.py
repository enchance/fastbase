from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from redis_om.connections import get_redis_connection
from decouple import config


DATABASE_URL = config('DATABASE_URL')
silent_engine = create_async_engine(DATABASE_URL)

app = FastAPI(docs_url=None, redoc_url=None, swagger_ui_oauth2_redirect_url=None)