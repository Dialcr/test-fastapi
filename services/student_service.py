from sqlalchemy.orm import Session
from models.student import Student
from models.user import User
from typing import List, Optional

class StudentService:
    def create_student(self, db: Session, email: str, password: str, first_name: str, 
                      last_name: str, student_id: str) -> Student:
        user = User(
            email=email,
            password=password,  # Remember to hash the password in production
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.flush()

        student = Student(
            user_id=user.id,
            student_id=student_id
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    def get_student(self, db: Session, student_id: int) -> Optional[Student]:
        return db.query(Student).filter(Student.id == student_id).first()

    def get_students(self, db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
        return db.query(Student).offset(skip).limit(limit).all()

    def update_student(self, db: Session, student_id: int, student_data: dict) -> Optional[Student]:
        student = self.get_student(db, student_id)
        if student:
            for key, value in student_data.items():
                if key in ['email', 'first_name', 'last_name']:
                    setattr(student.user, key, value)
                else:
                    setattr(student, key, value)
            db.commit()
            db.refresh(student)
        return student

    def delete_student(self, db: Session, student_id: int) -> bool:
        student = self.get_student(db, student_id)
        if student:
            db.delete(student.user)  # This will cascade delete the student
            db.commit()
            return True
        return False
