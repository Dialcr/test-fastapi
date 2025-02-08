from sqlalchemy.orm import Session
from models.qualification import Qualification
from models.user import User
from models.program import Program
from typing import List, Optional
from fastapi import HTTPException


class QualificationService:
    def create_qualification(self, db: Session, review: str, user_id: int, program_id: int, stars: int = 1) -> Qualification:
        user =  db.query(User).filter(user.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")

        program = db.query(Program).filter(Program.id == program_id).first()
        if program is None:
            raise HTTPException(status_code=400, detail="Program not found")
        if stars < 1 or stars > 5:
            raise HTTPException(status_code=400, detail="Stars must be between 1 and 5")
        
        qualification = Qualification(
            stars=stars,
            review=review,
            user_id=user_id,
            program_id=program_id
        )
        db.add(qualification)
        db.commit()
        db.refresh(qualification)
        return qualification

    def get_qualification(self, db: Session, qualification_id: int) -> Optional[Qualification]:
        return db.query(Qualification).filter(Qualification.id == qualification_id).first()

    def get_qualifications(self, db: Session, skip: int = 0, limit: int = 100) -> List[Qualification]:
        return db.query(Qualification).offset(skip).limit(limit).all()

    def update_qualification(self, db: Session, qualification_id: int, qualification_data: dict) -> Optional[Qualification]:
        qualification = self.get_qualification(db, qualification_id)
        if qualification:
            for key, value in qualification_data.items():
                setattr(qualification, key, value)
            db.commit()
            db.refresh(qualification)
        return qualification

    def delete_qualification(self, db: Session, qualification_id: int) -> bool:
        qualification = self.get_qualification(db, qualification_id)
        if qualification:
            db.delete(qualification)
            db.commit()
            return True
        return False
