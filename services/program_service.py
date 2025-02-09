from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.category import Category
from models.program import Program
from models.program_type import Program_type
from models.qualification import Qualification
from models.enrollment import Enrollment
from models.course import Course
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from schemas.category import CategoryResponse
from schemas.program import ProgramResponse
from schemas.program_type import ProgramTypeResponse


class ProgramService:
    def create_program(self, db: Session, name: str, description: str, duration_years: int, program_type_id: int, category_ids: List[int] = [], courses_ids: List[int] = []) -> Program:
        existing_program = db.query(Program).filter(Program.name == name).first()
        if existing_program is not None:
            raise HTTPException(status_code=400, detail="Program with the same name already exists")
        
        categories = db.query(Category).filter(Category.id.in_(category_ids)).all()
        if len(categories) != len(category_ids):
            raise HTTPException(status_code=400, detail="One or more categories not found")
        
        program_type = db.query(Program_type).filter(Program_type.id == program_type_id).first()
        if program_type is None:
            raise HTTPException(status_code=400, detail="Program type not found")
        courses = db.query(Course).filter(Course.id.in_(courses_ids)).all()
        if len(courses) != len(courses_ids):
            raise HTTPException(status_code=400, detail="One or more courses not found")
        
        program = Program(
            name=name,
            description=description,
            duration_years=duration_years,
            categories=categories,
            program_type_id=program_type.id,
            program_type=program_type,
            courses=courses
        )
        db.add(program)
        db.commit()
        db.refresh(program)
        return program

    def get_program(self, db: Session, program_id: int) -> Optional[Program]:
        return db.query(Program).filter(Program.id == program_id).first()

    def get_programs(self, db: Session, skip: int = 0, limit: int = 100, category_id: int = 0, popular: bool = False) -> List[ProgramResponse]:
        programs = db.query(
            Program,
            func.avg(Qualification.stars).label('avg_stars'),
            func.count(Enrollment.id).label('total_enrollments')
        ).outerjoin(
            Qualification, Qualification.program_id == Program.id
        ).outerjoin(
            Program.courses
        ).outerjoin(
            Enrollment, Enrollment.course_id == Course.id
        ).filter(or_(
            category_id == 0,
            Program.categories.any(id=category_id)
        )
        ).group_by(
            Program.id
        ).offset(skip).limit(limit).all()
        programs_response = [
            ProgramResponse(
                id=program.id,
                name=program.name,
                description=program.description,
                duration_years=program.duration_years,
                categories=[CategoryResponse(id=cat.id, name=cat.name, description=cat.description) for cat in program.categories],   
                program_type=ProgramTypeResponse(
                    id=program.program_type.id if program.program_type else 0,
                    name=program.program_type.name if program.program_type else ""
                ) if program.program_type else ProgramTypeResponse(id = 0, name = ""),  
                avg_stars=avg_stars or 0,  
                total_enrollments=total_enrollments
            )
            for program, avg_stars, total_enrollments in programs
        ]
        if popular:
            programs_response = sorted(programs_response, key=lambda x: x.avg_stars, reverse=True)
        return programs_response

    def get_programs_by_category(self, db: Session, skip: int = 0, limit: int = 100, category_id: int = 0) -> List[Program]:
        programs = db.query(
            Program,
            func.avg(Qualification.stars).label('avg_stars'),
            func.count(Enrollment.id).label('total_enrollments')
        ).outerjoin(
            Qualification, Qualification.program_id == Program.id
        ).outerjoin(
            Program.courses
        ).outerjoin(
            Enrollment, Enrollment.course_id == Course.id
        ).filter(or_(
            category_id == 0,
            Program.categories.any(id=category_id)
        )
        ).group_by(
            Program.id
        ).offset(skip).limit(limit).all()
        programs_response = [
            ProgramResponse(
                id=program.id,
                name=program.name,
                description=program.description,
                duration_years=program.duration_years,
                categories=[CategoryResponse(id=cat.id, name=cat.name, description=cat.description) for cat in program.categories],   
                program_type=ProgramTypeResponse(
                    id=program.program_type.id if program.program_type else 0,
                    name=program.program_type.name if program.program_type else ""
                ) if program.program_type else ProgramTypeResponse(id = 0, name = ""),  
                avg_stars=avg_stars or 0,  
                total_enrollments=total_enrollments
            )
            for program, avg_stars, total_enrollments in programs
        ]
        return sorted(programs_response, key=lambda x: x.avg_stars, reverse=True)


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
