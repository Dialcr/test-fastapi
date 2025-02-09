from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.professor import Professor
from models.subject import Subject
from models.user import User
from typing import List, Optional

from schemas.professor import ProfessorResponse

class ProfessorService:
    def create_professor(self, db: Session, email: str, password: str, first_name: str, 
                        last_name: str, department: str, description: str, subject_id: int) -> Professor:
        
        user = db.query(User).filter(User.email == email).first()
        if user is not None:
            raise HTTPException(status_code=400, detail="User with that email  already exists")
        
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if subject is None:
            raise HTTPException(status_code=400, detail="Subject not found")

        
        user = User(
            email=email,
            password=password,  # todo hash the password
            first_name=first_name,
            last_name=last_name,
        )
        db.add(user)
        db.flush()

        professor = Professor(
            user_id=user.id,
            department=department,
            description=description,
            user =user,
            subject_id=subject.id,
            subject=subject
        )
        db.add(professor)
        db.commit()
        db.refresh(professor)
        return ProfessorResponse(
            id=professor.id,
            department=professor.department,
            description=professor.description,
            email=professor.user.email,
            first_name=professor.user.first_name,
            last_name=professor.user.last_name
        )



    def get_professor(self, db: Session, professor_id: int) -> Optional[Professor]:
        return db.query(Professor).filter(Professor.id == professor_id
        ).outerjoin(
                Professor.user
            ).first()

    def get_professors(self, db: Session, skip: int = 0, limit: int = 100) -> List[Professor]:
        professors = db.query(Professor).outerjoin(
                Professor.user
            ).offset(skip).limit(limit).all()

        return [
            ProfessorResponse(
                id=professor.id,
                department=professor.department,
                description=professor.description,
                email=professor.user.email,
                first_name=professor.user.first_name,
                last_name=professor.user.last_name
            ) for professor in professors
        ]


    def update_professor(self, db: Session, professor_id: int, professor_data: dict) -> Optional[Professor]:
        professor = self.get_professor(db, professor_id)
        if professor:
            for key, value in professor_data.items():
                if key in ['email', 'first_name', 'last_name']:
                    setattr(professor.user, key, value)
                else:
                    setattr(professor, key, value)
            db.commit()
            db.refresh(professor)
        return professor

    def delete_professor(self, db: Session, professor_id: int) -> bool:
        professor = self.get_professor(db, professor_id)
        if professor:
            db.delete(professor.user)  # This will cascade delete the professor
            db.commit()
            return True
        return False
