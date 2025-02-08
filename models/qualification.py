from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .user import Base

class Qualification(Base):
    __tablename__ = "qualification"

    id = Column(Integer, primary_key=True, index=True)
    stars = Column(Integer, default=1)
    review = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))

    program = relationship("Program" ,back_populates="qualifications")
    user = relationship("User" ,back_populates="qualifications")
    