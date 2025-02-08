from sqlalchemy.orm import Session
from models.program import Program
from typing import List, Optional

class ProgramService:
    def create_program(self, db: Session, name: str, description: str, duration_years: int) -> Program:
        program = Program(
            name=name,
            description=description,
            duration_years=duration_years
        )
        db.add(program)
        db.commit()
        db.refresh(program)
        return program

    def get_program(self, db: Session, program_id: int) -> Optional[Program]:
        return db.query(Program).filter(Program.id == program_id).first()

    def get_programs(self, db: Session, skip: int = 0, limit: int = 100) -> List[Program]:
        return db.query(Program).offset(skip).limit(limit).all()

    def update_program(self, db: Session, program_id: int, program_data: dict) -> Optional[Program]:
        program = self.get_program(db, program_id)
        if program:
            for key, value in program_data.items():
                setattr(program, key, value)
            db.commit()
            db.refresh(program)
        return program

    def delete_program(self, db: Session, program_id: int) -> bool:
        program = self.get_program(db, program_id)
        if program:
            db.delete(program)
            db.commit()
            return True
        return False
