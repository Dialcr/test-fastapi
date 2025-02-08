from pydantic import BaseModel
from typing import Optional

class ProgramBase(BaseModel):
    name: str
    description: str
    duration_years: int

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_years: Optional[int] = None

class ProgramResponse(ProgramBase):
    id: int

    class Config:
        from_attributes = True
