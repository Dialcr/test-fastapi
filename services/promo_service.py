from sqlalchemy.orm import Session
from models.promo import Promo
from typing import List, Optional

class PromoService:
    def create_promo(self, db: Session, name: str, description: str) -> Promo:
        promo = Promo(name=name, description=description)
        db.add(promo)
        db.commit()
        db.refresh(promo)
        return promo

    def get_promo(self, db: Session, promo_id: int) -> Optional[Promo]:
        return db.query(Promo).filter(Promo.id == promo_id).first()

    def get_promos(self, db: Session, skip: int = 0, limit: int = 100) -> List[Promo]:
        return db.query(Promo).filter(Promo.activate).offset(skip).limit(limit).all()

    def update_promo(self, db: Session, promo_id: int, promo_data: dict) -> Optional[Promo]:
        promo = self.get_promo(db, promo_id)
        if promo:
            for key, value in promo_data.items():
                setattr(promo, key, value)
            db.commit()
            db.refresh(promo)
        return promo

    def delete_promo(self, db: Session, promo_id: int) -> bool:
        promo = self.get_promo(db, promo_id)
        if promo:
            db.delete(promo)
            db.commit()
            return True
        return False
