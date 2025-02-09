from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.course import Course
from typing import List, Optional
from datetime import datetime

from models.subject import Subject
from schemas.subject import SubjectBase

class CourseService:
    def create_course(self, db: Session, name: str, enrollment_start: datetime, enrollment_end: datetime, subjects: List[SubjectBase]) -> Course:

        created_subjects = []
        for subject_data in subjects:
            if subject_data.semester <= 0:
                raise HTTPException(status_code=400, detail="Semester must be greater than 0")
            subject = Subject(
                name=subject_data.name,
                description=subject_data.description,
                semester=subject_data.semester
            )
            db.add(subject)
            created_subjects.append(subject)

        course = Course(
            name=name,
            enrollment_start=enrollment_start,
            enrollment_end=enrollment_end,
            subjects=created_subjects
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    def get_course(self, db: Session, course_id: int) -> Optional[Course]:
        return db.query(Course).filter(Course.id == course_id).first()

    def get_courses(self, db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        return db.query(Course).offset(skip).limit(limit).all()

    def update_course(self, db: Session, course_id: int, course_data: dict) -> Optional[Course]:
        course = self.get_course(db, course_id)
        if course:
            for key, value in course_data.items():
                setattr(course, key, value)
            db.commit()
            db.refresh(course)
        return course

    def delete_course(self, db: Session, course_id: int) -> bool:
        course = self.get_course(db, course_id)
        if course:
            db.delete(course)
            db.commit()
            return True
        return False
