from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.promo_service import PromoService
from schemas.promo import PromoCreate, PromoUpdate, PromoResponse

router = APIRouter(prefix="/promos", tags=["promos"])
promo_service = PromoService()

@router.post("/", response_model=PromoResponse)
def create_promo(promo: PromoCreate, db: Session = Depends(get_db)):
    return promo_service.create_promo(db=db, name=promo.name, description=promo.description)

@router.get("/{promo_id}", response_model=PromoResponse)
def get_promo(promo_id: int, db: Session = Depends(get_db)):
    promo = promo_service.get_promo(db, promo_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    return promo

@router.get("/", response_model=List[PromoResponse])
def get_promos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return promo_service.get_promos(db, skip, limit)

@router.put("/{promo_id}", response_model=PromoResponse)
def update_promo(promo_id: int, promo: PromoUpdate, db: Session = Depends(get_db)):
    updated_promo = promo_service.update_promo(db, promo_id, promo.dict(exclude_unset=True))
    if not updated_promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    return updated_promo

@router.delete("/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    if not promo_service.delete_promo(db, promo_id):
        raise HTTPException(status_code=404, detail="Promo not found")
    return {"message": "Promo deleted successfully"}
