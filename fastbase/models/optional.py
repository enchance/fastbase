from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY

from .mixins import IntPK, UpdatedAtMixin
from ..utils import modstr



class TaxonomyMod(IntPK, SQLModel):
    name: str = Field(max_length=199)
    slug: str = Field(max_length=199)
    type: str = Field(max_length=50)
    sort: int | None = Field(default=1000)
    is_private: bool | None = Field(default=True)
    is_active: bool | None = Field(default=True)

    def __repr__(self):
        return modstr(self, 'name')


class OptionMod(IntPK, UpdatedAtMixin, SQLModel):
    key: str = Field(max_length=199)
    value: str = Field(max_length=255, nullable=True)

    # # Demo compound unique fields
    # xxx: str = Field(max_length=199)
    # yyy: str = Field(max_length=199)
    # __table_args__ = (UniqueConstraint('xxx', 'yyy'),)

    def __repr__(self):
        return modstr(self, 'key', 'val')
