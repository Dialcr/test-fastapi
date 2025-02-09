from pydantic import BaseModel
from typing import List, Optional
from schemas.category import CategoryResponse
from schemas.program_type import ProgramTypeResponse

class ProgramBase(BaseModel):
    name: str
    description: str
    duration_years: int

class ProgramCreate(ProgramBase):
    category_ids: List[int] = []
    courses_ids: List[int] = []
    program_type_id: int 
    pass

class ProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_years: Optional[int] = None

class ProgramResponse(ProgramBase):
    categories: list[CategoryResponse] = []
    program_type: ProgramTypeResponse
    avg_stars: float = 0
    total_enrollments: int = 0
    id: int

    class Config:
        from_attributes = True
