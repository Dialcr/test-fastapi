from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.qualification_service import QualificationService
from schemas.qualification import QualificationCreate, QualificationUpdate, QualificationResponse

router = APIRouter(prefix="/qualifications", tags=["qualifications"])
qualification_service = QualificationService()

@router.post("/", response_model=QualificationResponse)
def create_qualification(qualification: QualificationCreate, db: Session = Depends(get_db)):
    return qualification_service.create_qualification(
        db=db,
        stars=qualification.stars,
        review=qualification.review,
        user_id=qualification.user_id,
        program_id=qualification.program_id
    )

@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_qualification(qualification_id: int, db: Session = Depends(get_db)):
    qualification = qualification_service.get_qualification(db, qualification_id)
    if not qualification:
        raise HTTPException(status_code=404, detail="Qualification not found")
    return qualification

@router.get("/", response_model=List[QualificationResponse])
def get_qualifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return qualification_service.get_qualifications(db, skip, limit)

@router.put("/{qualification_id}", response_model=QualificationResponse)
def update_qualification(qualification_id: int, qualification: QualificationUpdate, db: Session = Depends(get_db)):
    updated_qualification = qualification_service.update_qualification(db, qualification_id, qualification.dict(exclude_unset=True))
    if not updated_qualification:
        raise HTTPException(status_code=404, detail="Qualification not found")
    return updated_qualification

@router.delete("/{qualification_id}")
def delete_qualification(qualification_id: int, db: Session = Depends(get_db)):
    if not qualification_service.delete_qualification(db, qualification_id):
        raise HTTPException(status_code=404, detail="Qualification not found")
    return {"message": "Qualification deleted successfully"}
