from sqlalchemy import Column
from sqlmodel import SQLModel, Field, String, JSON, Relationship
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import date

from .mixins import DTMixin, UuidPK
from ..utils import modstr


USER_TABLE = 'auth_user'
USER_PK = f'{USER_TABLE}.id'
author_fk = Field(foreign_key=USER_PK)
author_fk_nullable = Field(foreign_key=USER_PK, nullable=True)


class UserBase(SQLModel):
    username: str = Field(max_length=190, unique=True)
    email: str = Field(max_length=190)
    roles: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    groups: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    permissions: list[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    meta: dict = Field(sa_column=Column(JSON), default={})


class UserMod(DTMixin, UuidPK, UserBase):
    __tablename__ = USER_TABLE
    birthday: date | None = Field(nullable=True)
    gender: str | None = Field(max_length=20, nullable=True)

    def __str__(self):
        return modstr(self, 'username', 'email')