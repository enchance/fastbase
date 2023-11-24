from uuid import UUID
from pydantic import BaseModel



class FirebaseConfig(BaseModel):
    iss: str
    project_id: str


class UserObjectSchema(BaseModel):
    id: UUID
    email: str
    display: str
    username: str
    timezone: str
