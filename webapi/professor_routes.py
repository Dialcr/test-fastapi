from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.professor_service import ProfessorService
from schemas.professor import ProfessorCreate, ProfessorUpdate, ProfessorResponse

router = APIRouter(prefix="/professors", tags=["professors"])
professor_service = ProfessorService()

@router.post("/", response_model=ProfessorResponse)
def create_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    return professor_service.create_professor(
        db=db,
        email=professor.email,
        password=professor.password,
        first_name=professor.first_name,
        last_name=professor.last_name,
        department=professor.department,
        description=professor.description,
        subject_id=professor.subject_id
    )

@router.get("/{professor_id}", response_model=ProfessorResponse)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = professor_service.get_professor(db, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

@router.get("/", response_model=List[ProfessorResponse])
def get_professors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return professor_service.get_professors(db, skip, limit)

@router.put("/{professor_id}", response_model=ProfessorResponse)
def update_professor(professor_id: int, professor: ProfessorUpdate, db: Session = Depends(get_db)):
    updated_professor = professor_service.update_professor(db, professor_id, professor.dict(exclude_unset=True))
    if not updated_professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return updated_professor

@router.delete("/{professor_id}")
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    if not professor_service.delete_professor(db, professor_id):
        raise HTTPException(status_code=404, detail="Professor not found")
    return {"message": "Professor deleted successfully"}
