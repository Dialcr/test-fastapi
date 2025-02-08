
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .user import Base

class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    department = Column(String(100))
    description = Column(String(500))
    
    user = relationship("User")
    subjects = relationship("Subject", back_populates="professor")
