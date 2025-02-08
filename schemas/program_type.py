from pydantic import BaseModel
from typing import Optional

class ProgramTypeBase(BaseModel):
    name: str

class ProgramTypeCreate(ProgramTypeBase):
    pass

class ProgramTypeUpdate(BaseModel):
    name: Optional[str] = None

class ProgramTypeResponse(ProgramTypeBase):
    id: int

    class Config:
        from_attributes = True
