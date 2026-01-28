from fastapi import FastAPI, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

import app.models as models
import app.schemas as schemas
from app.database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

# ============= RATE LIMITER SETUP =============
limiter = Limiter(key_func=get_remote_address)

# FastAPI app
app = FastAPI(
    title="Vietnam Schools API",
    root_path="/openapi",
    description="Community-driven open API for Vietnamese universities and colleges",
    version="1.0.0",
    contact={
        "name": "Vietnam Schools API",
        "url": "https://github.com/ZenithHawking/schools-api",
    },
    license_info={
        "name": "MIT",
    },
)

# Attach rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/", tags=["Root"])
def root():
    """API Root - Welcome message"""
    return {
        "message": "Vietnam Schools API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "schools": "/api/v1/schools",
            "faculties": "/api/v1/faculties"
        },
        "github": "https://github.com/ZenithHawking/schools-api"
    }


# ============= SCHOOLS ENDPOINTS =============

@app.get("/api/v1/schools", response_model=List[schemas.School], tags=["Schools"])
@limiter.limit("100/minute")
def list_schools(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return"),
    code: Optional[str] = Query(None, description="Filter by exact school code"),
    country: Optional[str] = Query(None, description="Filter by country code (e.g., VN)"),
    type: Optional[str] = Query(None, description="Filter by type: public or private"),
    verified: Optional[bool] = Query(None, description="Filter by verification status"),
    search: Optional[str] = Query(None, description="Search in school name or code"),
    db: Session = Depends(get_db)
):
    """Get list of schools with filters (Rate limit: 100/minute)"""
    query = db.query(models.School)
    
    # Apply filters
    if code:
        query = query.filter(models.School.code == code.upper())
    if country:
        query = query.filter(models.School.country == country.upper())
    if type:
        query = query.filter(models.School.type == type.lower())
    if verified is not None:
        query = query.filter(models.School.verified == verified)
    if search:
        query = query.filter(
            or_(
                models.School.name.ilike(f"%{search}%"),
                models.School.code.ilike(f"%{search}%")
            )
        )
    
    schools = query.offset(skip).limit(limit).all()
    return schools


@app.get("/api/v1/schools/{school_id}", response_model=schemas.School, tags=["Schools"])
@limiter.limit("200/minute")
def get_school(
    request: Request,
    school_id: str, 
    db: Session = Depends(get_db)
):
    """Get school details by ID (Rate limit: 200/minute)"""
    school = db.query(models.School).filter(models.School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail=f"School with id '{school_id}' not found")
    return school


@app.post("/api/v1/schools", response_model=schemas.School, status_code=201, tags=["Schools"])
@limiter.limit("10/minute")
def create_school(
    request: Request,
    school: schemas.SchoolCreate, 
    db: Session = Depends(get_db)
):
    """Create a new school (Rate limit: 10/minute)"""
    # Check if school ID already exists
    existing = db.query(models.School).filter(models.School.id == school.id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"School with id '{school.id}' already exists")
    
    # Check if code already exists
    existing_code = db.query(models.School).filter(models.School.code == school.code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail=f"School with code '{school.code}' already exists")
    
    # Create school
    db_school = models.School(
        id=school.id,
        code=school.code,
        name=school.name,
        logo_url=school.logo_url,
        description=school.description,
        type=school.type,
        country=school.country,
        contact=school.contact.dict(),
        verified=school.metadata.verified,
        created_at=school.metadata.created_at,
        updated_at=school.metadata.updated_at
    )
    db.add(db_school)
    db.flush()
    
    # Create campuses
    for campus in school.campuses:
        db_campus = models.Campus(
            school_id=school.id,
            name=campus.name,
            address=campus.address,
            is_main=campus.is_main
        )
        db.add(db_campus)
    
    # Create faculties
    for faculty in school.faculties:
        db_faculty = models.Faculty(
            id=faculty.id,
            school_id=school.id,
            name=faculty.name,
            code=faculty.code,
            website=faculty.website,
            programs=faculty.programs
        )
        db.add(db_faculty)
    
    db.commit()
    db.refresh(db_school)
    return db_school


@app.put("/api/v1/schools/{school_id}", response_model=schemas.School, tags=["Schools"])
@limiter.limit("10/minute")
def update_school(
    request: Request,
    school_id: str, 
    school: schemas.SchoolCreate, 
    db: Session = Depends(get_db)
):
    """Update a school (Rate limit: 10/minute)"""
    db_school = db.query(models.School).filter(models.School.id == school_id).first()
    if not db_school:
        raise HTTPException(status_code=404, detail=f"School with id '{school_id}' not found")
    
    # Update school fields
    db_school.code = school.code
    db_school.name = school.name
    db_school.logo_url = school.logo_url
    db_school.description = school.description
    db_school.type = school.type
    db_school.country = school.country
    db_school.contact = school.contact.dict()
    db_school.verified = school.metadata.verified
    db_school.updated_at = school.metadata.updated_at
    
    # Delete old campuses and faculties
    db.query(models.Campus).filter(models.Campus.school_id == school_id).delete()
    db.query(models.Faculty).filter(models.Faculty.school_id == school_id).delete()
    
    # Add new campuses
    for campus in school.campuses:
        db_campus = models.Campus(
            school_id=school_id,
            name=campus.name,
            address=campus.address,
            is_main=campus.is_main
        )
        db.add(db_campus)
    
    # Add new faculties
    for faculty in school.faculties:
        db_faculty = models.Faculty(
            id=faculty.id,
            school_id=school_id,
            name=faculty.name,
            code=faculty.code,
            website=faculty.website,
            programs=faculty.programs
        )
        db.add(db_faculty)
    
    db.commit()
    db.refresh(db_school)
    return db_school


@app.delete("/api/v1/schools/{school_id}", tags=["Schools"])
@limiter.limit("10/minute")
def delete_school(
    request: Request,
    school_id: str, 
    db: Session = Depends(get_db)
):
    """Delete a school (Rate limit: 10/minute)"""
    db_school = db.query(models.School).filter(models.School.id == school_id).first()
    if not db_school:
        raise HTTPException(status_code=404, detail=f"School with id '{school_id}' not found")
    
    db.delete(db_school)
    db.commit()
    return {"message": f"School '{school_id}' deleted successfully"}


# ============= FACULTIES ENDPOINTS =============

@app.get("/api/v1/faculties", response_model=List[schemas.FacultyList], tags=["Faculties"])
@limiter.limit("50/minute")
def list_faculties(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    school_id: Optional[str] = Query(None, description="Filter by school ID"),
    search: Optional[str] = Query(None, description="Search in faculty name or code"),
    db: Session = Depends(get_db)
):
    """Get list of faculties with filters (Rate limit: 50/minute)"""
    query = db.query(models.Faculty)
    
    if school_id:
        query = query.filter(models.Faculty.school_id == school_id)
    if search:
        query = query.filter(
            or_(
                models.Faculty.name.ilike(f"%{search}%"),
                models.Faculty.code.ilike(f"%{search}%")
            )
        )
    
    faculties = query.offset(skip).limit(limit).all()
    return faculties


@app.get("/api/v1/faculties/{faculty_id}", response_model=schemas.Faculty, tags=["Faculties"])
@limiter.limit("200/minute")
def get_faculty(
    request: Request,
    faculty_id: str, 
    db: Session = Depends(get_db)
):
    """Get faculty details by ID (Rate limit: 200/minute)"""
    faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail=f"Faculty with id '{faculty_id}' not found")
    return faculty


@app.get("/api/v1/schools/{school_id}/faculties", response_model=List[schemas.Faculty], tags=["Schools", "Faculties"])
@limiter.limit("100/minute")
def get_school_faculties(
    request: Request,
    school_id: str, 
    db: Session = Depends(get_db)
):
    """Get all faculties of a specific school (Rate limit: 100/minute)"""
    # Check if school exists
    school = db.query(models.School).filter(models.School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail=f"School with id '{school_id}' not found")
    
    faculties = db.query(models.Faculty).filter(models.Faculty.school_id == school_id).all()
    return faculties


@app.get("/api/v1/schools/{school_id}/campuses", response_model=List[schemas.Campus], tags=["Schools", "Campuses"])
@limiter.limit("100/minute")
def get_school_campuses(
    request: Request,
    school_id: str, 
    db: Session = Depends(get_db)
):
    """Get all campuses of a specific school (Rate limit: 100/minute)"""
    # Check if school exists
    school = db.query(models.School).filter(models.School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail=f"School with id '{school_id}' not found")
    
    campuses = db.query(models.Campus).filter(models.Campus.school_id == school_id).all()
    return campuses