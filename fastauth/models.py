import sqlalchemy as sa
from uuid import UUID, uuid4
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Session, text, select, JSON, String, Relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY

from .utils import modstr


USER_TABLE = 'auth_user'
USER_PK = f'{USER_TABLE}.id'
author_fk = Field(foreign_key=USER_PK)
author_fk_nullable = Field(foreign_key=USER_PK, nullable=True)


class UpdatedAtMixin(SQLModel):
    updated_at: datetime | None = Field(sa_column=sa.Column(sa.DateTime(timezone=True),
                                                            server_default=text('CURRENT_TIMESTAMP'),
                                                            server_onupdate=text('CURRENT_TIMESTAMP')))     # noqa


class CreatedAtMixin(SQLModel):
    created_at: datetime | None = Field(sa_column=sa.Column(sa.DateTime(timezone=True),
                                                            server_default=text('CURRENT_TIMESTAMP')))


class DeletedAtMixin(SQLModel):
    deleted_at: datetime | None = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True))


class DTMixin(CreatedAtMixin, UpdatedAtMixin, DeletedAtMixin, SQLModel):
    pass


class IntPK(SQLModel):
    id: int | None = Field(primary_key=True, default=None)


class UuidPK(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class UserBase(SQLModel):
    username: str = Field(max_length=190, unique=True)
    email: str = Field(max_length=190)
    permissions: list[str] = Field(sa_column=sa.Column(ARRAY(String)), default=[])
    meta: dict = Field(sa_column=sa.Column(JSON), default={})


class UserMod(DTMixin, UuidPK, UserBase):
    __tablename__ = USER_TABLE
    birthday: date | None = Field(nullable=True)
    gender: str | None = Field(max_length=20, nullable=True)

    def __str__(self):
        return modstr(self, 'username', 'email')


class Group(IntPK, SQLModel, table=True):
    __tablename__ = 'auth_group'
    name: str = Field(max_length=20, unique=True)
    permissions: list[str] = Field(sa_column=sa.Column(ARRAY(String)), default=[])

    def __str__(self):
        return modstr(self, 'name')


class Role(IntPK, SQLModel, table=True):
    __tablename__ = 'auth_role'
    name: str = Field(max_length=20, unique=True)
    description: str | None = Field(max_length=199, default='')
    groups: list[str] = Field(sa_column=sa.Column(ARRAY(String)), default=[])

    def __str__(self):
        return modstr(self, 'name', 'description')


class TaxonomyMod(IntPK, SQLModel):
    name: str = Field(max_length=199)
    type: str = Field(max_length=20)
    sort: int | None = Field(default=1000)
    is_private: bool | None = Field(default=False)
    is_active: bool | None = Field(default=True)
    author_id: UUID = author_fk

    author: 'User' = Relationship(back_populates='author_tax')       # noqa

    def __str__(self):
        return modstr(self, 'name')


class OptionMod(UpdatedAtMixin, SQLModel):
    author_id: UUID = Field(primary_key=True)
    key: str = Field(max_length=20, primary_key=True)
    val: str = Field(max_length=199, nullable=True)

    author: 'User' = Relationship(back_populates='author_options')       # noqa

    # # Demo compound unique fields
    # xxx: str = Field(max_length=199)
    # yyy: str = Field(max_length=199)
    # __table_args__ = (UniqueConstraint('xxx', 'yyy'),)

    def __str__(self):
        return modstr(self, 'key')
