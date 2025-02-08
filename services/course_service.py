from sqlalchemy.orm import Session
from models.course import Course
from typing import List, Optional
from datetime import datetime

class CourseService:
    def create_course(self, db: Session, program_id: int, name: str, enrollment_start: datetime, enrollment_end: datetime) -> Course:
        course = Course(
            program_id=program_id,
            name=name,
            enrollment_start=enrollment_start,
            enrollment_end=enrollment_end
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
