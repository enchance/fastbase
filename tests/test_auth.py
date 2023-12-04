import pytest
from sqlmodel import select

from .testapp.main import User
from fastbase import ic
from fastbase.models import Group


class TestGroup:
    async def test_foo(self, session):
        # count_stmt = select(Group)
        # stmt = select(Group)
        # execdata = await session.exec(count_stmt)
        # data = execdata.all()
        # ic(data)
        # assert data
        assert True