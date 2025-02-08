from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CourseBase(BaseModel):
    name: str
    program_id: int
    enrollment_start: datetime
    enrollment_end: datetime

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    program_id: Optional[int] = None
    enrollment_start: Optional[datetime] = None
    enrollment_end: Optional[datetime] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True
