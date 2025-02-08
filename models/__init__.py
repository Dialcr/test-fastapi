from models.user import Base
from models.professor import Professor
from models.student import Student
from models.program import Program, program_courses
from models.course import Course
from models.subject import Subject
from models.enrollment import Enrollment
from models.review import Review
from models.category import Category, program_categories
from models.program_type import Program_type
from models.qualification import Qualification

__all__ = [
    'Base',
    'Professor',
    'Student', 
    'Program',
    'Course',
    'Subject',
    'Enrollment',
    'Review',
    'Category',
    'program_categories',
    'Program_type',
    'Qualification',
    'program_courses',
]
