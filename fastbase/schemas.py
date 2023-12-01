from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel
from enum import StrEnum, auto



class GroupEnum(StrEnum):
    AdminGroup = 'AdminGroup'
    AccountGroup = 'AccountGroup'


class UserBaseSchema(BaseModel):
    id: UUID
    email: str
    display: str
    username: str
    timezone: str
    birthday: date | None
    created_at: datetime