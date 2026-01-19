from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict


# Contact Schema
class Contact(BaseModel):
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


# Campus Schemas
class CampusBase(BaseModel):
    name: str
    address: str
    is_main: bool = False

class Campus(CampusBase):
    id: int
    school_id: str
    
    class Config:
        from_attributes = True


# Faculty Schemas
class FacultyBase(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    website: Optional[str] = None
    programs: List[str] = []

class Faculty(FacultyBase):
    school_id: str
    
    class Config:
        from_attributes = True


# Metadata Schema
class Metadata(BaseModel):
    verified: bool = False
    created_at: str
    updated_at: str


# School Schemas
class SchoolBase(BaseModel):
    id: str
    code: str
    name: str
    logo_url: Optional[str] = None
    description: str
    type: str  # public/private
    country: str = "VN"
    contact: Contact

class SchoolCreate(SchoolBase):
    campuses: List[CampusBase]
    faculties: List[FacultyBase]
    metadata: Metadata

class School(SchoolBase):
    campuses: List[Campus] = []
    faculties: List[Faculty] = []
    verified: bool
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


# Response schemas for lists
class SchoolList(BaseModel):
    id: str
    code: str
    name: str
    type: str
    country: str
    verified: bool
    
    class Config:
        from_attributes = True


class FacultyList(BaseModel):
    id: str
    name: str
    code: Optional[str]
    school_id: str
    
    class Config:
        from_attributes = True
