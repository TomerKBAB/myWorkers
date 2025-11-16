# DB schema & queries
from pydantic import BaseModel

class JobCreate(BaseModel):
    type: str
    payload: dict