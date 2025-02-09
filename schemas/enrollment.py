from pydantic import BaseModel
from datetime import datetime

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrollment_date: datetime

    class Config:
        from_attributes = True
