from pydantic import BaseModel
from typing import Optional

class PromoBase(BaseModel):
    name: str
    description: str

class PromoCreate(PromoBase):
    pass

class PromoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PromoResponse(PromoBase):
    id: int

    class Config:
        from_attributes = True
