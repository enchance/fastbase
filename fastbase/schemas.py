from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel



class UserBaseSchema(BaseModel):
    id: UUID
    email: str
    display: str
    timezone: str
    created_at: datetime
    banned_at: bool | None = None
    role: str