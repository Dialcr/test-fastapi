
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .user import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(str(20), unique=True)
    
    user = relationship("User")
    enrollments = relationship("Enrollment", back_populates="student")
