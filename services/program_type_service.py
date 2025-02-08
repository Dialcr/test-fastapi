from sqlalchemy.orm import Session
from models.program_type import Program_type
from typing import List, Optional

class ProgramTypeService:
    def create_program_type(self, db: Session, name: str) -> Program_type:
        program_type = Program_type(name=name)
        db.add(program_type)
        db.commit()
        db.refresh(program_type)
        return program_type

    def get_program_type(self, db: Session, program_type_id: int) -> Optional[Program_type]:
        return db.query(Program_type).filter(Program_type.id == program_type_id).first()

    def get_program_types(self, db: Session, skip: int = 0, limit: int = 100) -> List[Program_type]:
        return db.query(Program_type).offset(skip).limit(limit).all()

    def update_program_type(self, db: Session, program_type_id: int, program_type_data: dict) -> Optional[Program_type]:
        program_type = self.get_program_type(db, program_type_id)
        if program_type:
            for key, value in program_type_data.items():
                setattr(program_type, key, value)
            db.commit()
            db.refresh(program_type)
        return program_type

    def delete_program_type(self, db: Session, program_type_id: int) -> bool:
        program_type = self.get_program_type(db, program_type_id)
        if program_type:
            db.delete(program_type)
            db.commit()
            return True
        return False
