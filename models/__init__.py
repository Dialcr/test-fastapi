
from models.user import Base
from models.professor import Professor
from models.student import Student
from models.program import Program
from models.course import Course
from models.subject import Subject
from models.enrollment import Enrollment
from models.review import Review

__all__ = [
    'Base',
    'Professor',
    'Student', 
    'Program',
    'Course',
    'Subject',
    'Enrollment',
    'Review'
]
