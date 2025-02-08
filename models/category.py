from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

program_categories = Table(
    'program_categories',
    Base.metadata,
    Column('program_id', Integer, ForeignKey('programs.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    
    programs = relationship("Program", secondary=program_categories, back_populates="categories")
