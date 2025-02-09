from pydantic import BaseModel, EmailStr
from typing import Optional

class SubjectBase(BaseModel):
    name: str
    description: str
    semester: int

class SubjectResponse(SubjectBase):
    id: int