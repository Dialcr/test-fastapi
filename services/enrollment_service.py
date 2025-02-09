from sqlalchemy.orm import Session
from models.enrollment import Enrollment
from models.student import Student
from models.course import Course
from typing import List, Optional
from fastapi import HTTPException
from datetime import datetime

class EnrollmentService:
    def create_enrollment(self, db: Session, student_id: int, course_id: int) -> Enrollment:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Verify course exists and enrollment period
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        current_date = datetime.utcnow()
        if current_date < course.enrollment_start or current_date > course.enrollment_end:
            raise HTTPException(status_code=400, detail="Course enrollment period is not active")

        # Check if student is already enrolled
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        ).first()
        if existing_enrollment:
            raise HTTPException(status_code=400, detail="Student already enrolled in this course")

        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    def get_enrollment(self, db: Session, enrollment_id: int) -> Optional[Enrollment]:
        return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

    def get_enrollments(self, db: Session, skip: int = 0, limit: int = 100) -> List[Enrollment]:
        return db.query(Enrollment).offset(skip).limit(limit).all()

    def delete_enrollment(self, db: Session, enrollment_id: int) -> bool:
        enrollment = self.get_enrollment(db, enrollment_id)
        if enrollment:
            db.delete(enrollment)
            db.commit()
            return True
        return False
