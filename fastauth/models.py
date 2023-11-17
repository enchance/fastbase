import sqlalchemy as sa
from uuid import UUID, uuid4
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Session, text, select, JSON, String
from sqlalchemy.dialects.postgresql import ARRAY

from .utils import modstr



class DTMixin(SQLModel):
    deleted_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True))
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False,
                                                     server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False,
                                                     server_default=text('CURRENT_TIMESTAMP'),
                                                     server_onupdate=text('CURRENT_TIMESTAMP')))


class IntPK(SQLModel):
    id: int | None = Field(primary_key=True, default=None)


class UuidPK(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class AccountBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(max_length=190, unique=True)
    email: str = Field(max_length=190, nullable=False)


class Account(DTMixin, UuidPK, AccountBase, table=True):
    __tablename__ = 'auth_user'
    birthday: date | None = Field(nullable=True)
    gender: str = Field(max_length=20, nullable=True)
    permissions: list[str] = Field(sa_column=sa.Column(ARRAY(String)), default=[])
    meta: dict = Field(sa_column=sa.Column(JSON), default={})

    def __str__(self):
        return modstr(self, 'username', 'email')


class Group(IntPK, SQLModel, table=True):
    __tablename__ = 'auth_group'
    name: str = Field(max_length=20, unique=True)
    permissions: list[str] = Field(sa_column=sa.Column(ARRAY(String)), default=[])
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False,
                                                     server_default=text('CURRENT_TIMESTAMP')))

    def __str__(self):
        return modstr(self, 'name')