from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    student_id: str

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    student_id: Optional[str] = None

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
