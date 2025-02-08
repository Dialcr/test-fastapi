from sqlalchemy.orm import Session
from models.category import Category
from typing import List, Optional

class CategoryService:
    def create_category(self, db: Session, name: str, description: str) -> Category:
        category = Category(name=name, description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def get_category(self, db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()

    def get_categories(self, db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        return db.query(Category).offset(skip).limit(limit).all()

    def update_category(self, db: Session, category_id: int, category_data: dict) -> Optional[Category]:
        category = self.get_category(db, category_id)
        if category:
            for key, value in category_data.items():
                setattr(category, key, value)
            db.commit()
            db.refresh(category)
        return category

    def delete_category(self, db: Session, category_id: int) -> bool:
        category = self.get_category(db, category_id)
        if category:
            db.delete(category)
            db.commit()
            return True
        return False

    def add_program_to_category(self, db: Session, category_id: int, program_id: int) -> Optional[Category]:
        from models.program import Program
        category = self.get_category(db, category_id)
        program = db.query(Program).filter(Program.id == program_id).first()
        if category and program:
            category.programs.append(program)
            db.commit()
            db.refresh(category)
        return category

    def remove_program_from_category(self, db: Session, category_id: int, program_id: int) -> Optional[Category]:
        from models.program import Program
        category = self.get_category(db, category_id)
        program = db.query(Program).filter(Program.id == program_id).first()
        if category and program and program in category.programs:
            category.programs.remove(program)
            db.commit()
            db.refresh(category)
        return category
