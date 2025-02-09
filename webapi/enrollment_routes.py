from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.enrollment_service import EnrollmentService
from schemas.enrollment import EnrollmentCreate, EnrollmentResponse

router = APIRouter(prefix="/enrollments", tags=["enrollments"])
enrollment_service = EnrollmentService()

@router.post("/", response_model=EnrollmentResponse)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    return enrollment_service.create_enrollment(
        db=db,
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = enrollment_service.get_enrollment(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@router.get("/", response_model=List[EnrollmentResponse])
def get_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return enrollment_service.get_enrollments(db, skip, limit)

@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    if not enrollment_service.delete_enrollment(db, enrollment_id):
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"message": "Enrollment deleted successfully"}
