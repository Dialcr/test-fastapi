from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .user import Base

class Promo(Base):
    __tablename__ = "promos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(String(500))
    activate = Column(Boolean, default=True)
