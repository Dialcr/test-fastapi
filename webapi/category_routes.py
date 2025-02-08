from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.category_service import CategoryService
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])
category_service = CategoryService()

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(
        db=db,
        name=category.name,
        description=category.description
    )

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return category_service.get_categories(db, skip, limit)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = category_service.update_category(db, category_id, category.dict(exclude_unset=True))
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if not category_service.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

@router.post("/{category_id}/programs/{program_id}")
def add_program_to_category(category_id: int, program_id: int, db: Session = Depends(get_db)):
    category = category_service.add_program_to_category(db, category_id, program_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category or Program not found")
    return {"message": "Program added to category successfully"}

@router.delete("/{category_id}/programs/{program_id}")
def remove_program_from_category(category_id: int, program_id: int, db: Session = Depends(get_db)):
    category = category_service.remove_program_from_category(db, category_id, program_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category or Program not found")
    return {"message": "Program removed from category successfully"}
