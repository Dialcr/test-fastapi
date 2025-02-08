from sqlalchemy.orm import Session
from models.professor import Professor
from models.user import User
from typing import List, Optional

class ProfessorService:
    def create_professor(self, db: Session, email: str, password: str, first_name: str, 
                        last_name: str, department: str) -> Professor:
        user = User(
            email=email,
            password=password,  # Remember to hash the password in production
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.flush()

        professor = Professor(
            user_id=user.id,
            department=department
        )
        db.add(professor)
        db.commit()
        db.refresh(professor)
        return professor

    def get_professor(self, db: Session, professor_id: int) -> Optional[Professor]:
        return db.query(Professor).filter(Professor.id == professor_id).first()

    def get_professors(self, db: Session, skip: int = 0, limit: int = 100) -> List[Professor]:
        return db.query(Professor).offset(skip).limit(limit).all()

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
