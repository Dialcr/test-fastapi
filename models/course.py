from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .user import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    name = Column(String(200))
    enrollment_start = Column(DateTime)
    enrollment_end = Column(DateTime)
    
    program = relationship("Program", back_populates="courses")
    subjects = relationship("Subject", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    reviews = relationship("Review", back_populates="course")
