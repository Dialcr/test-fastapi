from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .user import Base


program_courses = Table(
    'program_course',
    Base.metadata,
    Column('program_id', Integer, ForeignKey('programs.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(String(500))
    duration_years = Column(Integer)
    program_type_id = Column(Integer, ForeignKey("program_types.id"))

    program_type = relationship("Program_type", back_populates="programs")
    courses = relationship("Course", secondary="program_course", back_populates="programs")
    categories = relationship("Category", secondary="program_categories", back_populates="programs")
    qualifications = relationship("Qualification", back_populates="program")

