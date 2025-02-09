from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ProfessorBase(BaseModel):
    # email: EmailStr
    email: EmailStr = Field(alias='user.email')
    first_name: str = Field(alias='user.first_name')
    last_name: str = Field(alias='user.last_name')
    department: str
    description: str

class ProfessorCreate(ProfessorBase):
    password: str
    subject_id: int

class ProfessorUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None

class ProfessorResponse(ProfessorBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True
