from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel



class FirebaseConfig(BaseModel):
    iss: str
    project_id: str


class UserSchema(BaseModel):
    id: UUID
    email: str
    display: str
    username: str
    timezone: str
    birthday: date | None
    created_at: datetime
