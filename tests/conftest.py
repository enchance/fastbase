import pytest, asyncio, httpx, pytest_asyncio
from typing import Generator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from decouple import config

from fastbase import ic
from tests.testapp.main import app
from .seed import seed_groups, seed_roles


TESTDB_URL = config('TESTDB_URL')
silent_engine = create_async_engine(TESTDB_URL, pool_size=10, echo=False, future=True)
