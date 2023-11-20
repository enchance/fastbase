from sqlmodel import SQLModel, Field, String
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY

from .mixins import IntPK
from ..utils import modstr


class Group(IntPK, SQLModel, table=True):
    __tablename__ = 'auth_group'
    name: str = Field(max_length=20, unique=True)
    description: str = Field(max_length=199, default='')
    permissions: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])

    def __str__(self):
        return modstr(self, 'name')