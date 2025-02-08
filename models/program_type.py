from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .user import Base

class Program_type(Base):
    __tablename__ = "program_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    programs = relationship("Program" ,back_populates="program_type")

