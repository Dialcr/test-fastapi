from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .user import Base

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(String(500))
    duration_years = Column(Integer)
    
    courses = relationship("Course", back_populates="program")
