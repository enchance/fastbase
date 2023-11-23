from pydantic import BaseModel



class FirebaseConfig(BaseModel):
    iss: str
    project_id: str