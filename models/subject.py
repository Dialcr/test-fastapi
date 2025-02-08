from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .user import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    professor_id = Column(Integer, ForeignKey("professors.id"))
    name = Column(String(200))
    description = Column(String(500))
    semester = Column(Integer)
    
    course = relationship("Course", back_populates="subjects")
    professor = relationship("Professor", back_populates="subjects")
