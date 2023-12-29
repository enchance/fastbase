from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, text
from sqlalchemy import Column, DateTime



class UpdatedAtMixin(SQLModel):
    updated_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True),
                                                         server_default=text('CURRENT_TIMESTAMP'),
                                                         server_onupdate=text('CURRENT_TIMESTAMP')))     # noqa


class CreatedAtMixin(SQLModel):
    created_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True),
                                                         server_default=text('CURRENT_TIMESTAMP')))


class DeletedAtMixin(SQLModel):
    deleted_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))


class DTMixin(CreatedAtMixin, UpdatedAtMixin, SQLModel):
    pass


class IntPK(SQLModel):
    id: int | None = Field(primary_key=True, default=None)


class UuidPK(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)