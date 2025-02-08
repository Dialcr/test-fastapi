from pydantic import BaseModel
from typing import Optional

class QualificationBase(BaseModel):
    stars: int
    review: str
    user_is: int
    program_id: int

class QualificationCreate(QualificationBase):
    pass

class QualificationUpdate(BaseModel):
    stars: Optional[int] = None
    review: Optional[str] = None
    user_is: Optional[int] = None
    program_id: Optional[int] = None

class QualificationResponse(QualificationBase):
    id: int

    class Config:
        from_attributes = True
