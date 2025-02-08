from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.program_service import ProgramService
from schemas.program import ProgramCreate, ProgramUpdate, ProgramResponse

router = APIRouter(prefix="/programs", tags=["programs"])
program_service = ProgramService()

@router.post("/", response_model=ProgramResponse)
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    resutl =program_service.create_program(
        db=db,
        name=program.name,
        description=program.description,
        duration_years=program.duration_years,
        category_ids=program.category_ids,
        program_type_id=program.program_type_id
    )
    return resutl 
        
@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(program_id: int, db: Session = Depends(get_db)):
    program = program_service.get_program(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.get("/", response_model=List[ProgramResponse])
def get_programs(skip: int = 0, limit: int = 100,category_id: int = 0,popular: bool = False, db: Session = Depends(get_db)):
    return program_service.get_programs(db, skip, limit, popular=popular, category_id=category_id)

# @router.get("/categories/{category_id}", response_model=List[ProgramResponse])
# def get_programs_by_category(skip: int = 0, limit: int = 100, category_id: int = 0, db: Session = Depends(get_db)):
#     return program_service.get_programs_by_category(db, skip, limit, category_id)


@router.put("/{program_id}", response_model=ProgramResponse)
def update_program(program_id: int, program: ProgramUpdate, db: Session = Depends(get_db)):
    updated_program = program_service.update_program(db, program_id, program.dict(exclude_unset=True))
    if not updated_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return updated_program

@router.delete("/{program_id}")
def delete_program(program_id: int, db: Session = Depends(get_db)):
    if not program_service.delete_program(db, program_id):
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted successfully"}
