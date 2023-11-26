from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY

from .mixins import IntPK, UpdatedAtMixin
from .UserMod import author_fk
from ..utils import modstr



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
