from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.program_type_service import ProgramTypeService
from schemas.program_type import ProgramTypeCreate, ProgramTypeUpdate, ProgramTypeResponse

router = APIRouter(prefix="/program-types", tags=["program-types"])
program_type_service = ProgramTypeService()

@router.post("/", response_model=ProgramTypeResponse)
def create_program_type(program_type: ProgramTypeCreate, db: Session = Depends(get_db)):
    return program_type_service.create_program_type(
        db=db,
        name=program_type.name
    )

@router.get("/{program_type_id}", response_model=ProgramTypeResponse)
def get_program_type(program_type_id: int, db: Session = Depends(get_db)):
    program_type = program_type_service.get_program_type(db, program_type_id)
    if not program_type:
        raise HTTPException(status_code=404, detail="Program type not found")
    return program_type

@router.get("/", response_model=List[ProgramTypeResponse])
def get_program_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return program_type_service.get_program_types(db, skip, limit)

@router.put("/{program_type_id}", response_model=ProgramTypeResponse)
def update_program_type(program_type_id: int, program_type: ProgramTypeUpdate, db: Session = Depends(get_db)):
    updated_program_type = program_type_service.update_program_type(db, program_type_id, program_type.dict(exclude_unset=True))
    if not updated_program_type:
        raise HTTPException(status_code=404, detail="Program type not found")
    return updated_program_type

@router.delete("/{program_type_id}")
def delete_program_type(program_type_id: int, db: Session = Depends(get_db)):
    if not program_type_service.delete_program_type(db, program_type_id):
        raise HTTPException(status_code=404, detail="Program type not found")
    return {"message": "Program type deleted successfully"}
