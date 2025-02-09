from webapi.course_routes import router as course_routes
from webapi.program_routes import router as program_routes
from webapi.student_routes import router as student_routes
from webapi.professor_routes import router as professor_routes
from webapi.category_routes import router as category_routes
from webapi.qualification_routes import router as qualification_routes
from webapi.program_type_routes import router as program_type_routes
from webapi.promo_routes import router as promo_routes
from webapi.enrollment_routes import router as enrollment_routes


__all__ = [
    'course_routes',
    'program_routes',
    'student_routes',
    'professor_routes',
    'category_routes',
    'qualification_routes',
    'program_type_routes',
    'promo_routes',
    'enrollment_routes'
]
