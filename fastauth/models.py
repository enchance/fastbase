import sqlalchemy as sa
from uuid import UUID, uuid4
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Session, text, select, JSON



class DTMixin(SQLModel):
    deleted_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True))
    created_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False,
                                                     server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False,
                                                     server_default=text('CURRENT_TIMESTAMP'),
                                                     server_onupdate=text('CURRENT_TIMESTAMP')))


class AccountBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(max_length=190, unique=True)
    email: str = Field(max_length=190, nullable=False)


class Account(DTMixin, AccountBase, table=True):
    __tablename__ = 'app_user'
    birthday: date | None = Field(nullable=True)
    gender: str = Field(max_length=20, nullable=True)
    meta: dict = Field(sa_column=sa.Column(JSON, default={}))

    def __str__(self):
        return f'{self.username} <{self.email}> {self.id}'