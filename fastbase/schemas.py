from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel
from enum import StrEnum, auto



class FirebaseConfig(BaseModel):
    iss: str
    project_id: str


class GroupEnum(StrEnum):
    AdminGroup = 'AdminGroup'
    AccountGroup = 'AccountGroup'


class UserBaseSchema(BaseModel):
    id: UUID
    email: str
    display: str
    username: str
    timezone: str
    created_at: datetime