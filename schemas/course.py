from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from schemas.subject import SubjectBase

class CourseBase(BaseModel):
    name: str
    enrollment_start: datetime
    enrollment_end: datetime

class CourseCreate(CourseBase):
    subjects: list[SubjectBase]
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    program_id: Optional[int] = None
    enrollment_start: Optional[datetime] = None
    enrollment_end: Optional[datetime] = None

class CourseResponse(CourseBase):
    subjects: list[SubjectBase] = []
    id: int

    class Config:
        from_attributes = True
