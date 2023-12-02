from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY

from .mixins import IntPK, UpdatedAtMixin
from ..utils import modstr



class TaxonomyMod(IntPK, SQLModel):
    name: str = Field(max_length=199)
    type: str = Field(max_length=20)
    sort: int | None = Field(default=1000)
    is_private: bool | None = Field(default=False)
    is_active: bool | None = Field(default=True)

    def __repr__(self):
        return modstr(self, 'name')


class OptionMod(UpdatedAtMixin, IntPK, SQLModel):
    key: str = Field(max_length=20, primary_key=True)
    val: str = Field(max_length=199, nullable=True)

    # # Demo compound unique fields
    # xxx: str = Field(max_length=199)
    # yyy: str = Field(max_length=199)
    # __table_args__ = (UniqueConstraint('xxx', 'yyy'),)

    def __repr__(self):
        return modstr(self, 'key')
