from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from webapi import course_routes, program_routes, student_routes, professor_routes, category_routes, qualification_routes, program_type_routes, promo_routes, enrollment_routes
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    # allow_origins=["https://example.com", "https://frontend.com"],  
    # allow_origins=[os.getenv('ORIGIN_URL_FRONTEND'), os.getenv('ORIGIN_URL')],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(course_routes)
app.include_router(program_routes)
app.include_router(student_routes)
app.include_router(professor_routes)
app.include_router(category_routes)
app.include_router(qualification_routes)
app.include_router(program_type_routes)
app.include_router(promo_routes)
app.include_router(enrollment_routes)


