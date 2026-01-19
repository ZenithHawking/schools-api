from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class School(Base):
    __tablename__ = "schools"
    
    id = Column(String, primary_key=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    logo_url = Column(String(500))
    description = Column(Text)
    type = Column(String(20), nullable=False)  # public/private
    country = Column(String(2), nullable=False, default="VN")
    
    # Contact stored as JSON
    contact = Column(JSON)  # {"website": "...", "email": "...", "phone": "..."}
    
    # Metadata
    verified = Column(Boolean, default=False)
    created_at = Column(String(50))
    updated_at = Column(String(50))
    
    # Relationships
    campuses = relationship("Campus", back_populates="school", cascade="all, delete-orphan")
    faculties = relationship("Faculty", back_populates="school", cascade="all, delete-orphan")


class Campus(Base):
    __tablename__ = "campuses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(String, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    is_main = Column(Boolean, default=False)
    
    school = relationship("School", back_populates="campuses")


class Faculty(Base):
    __tablename__ = "faculties"
    
    id = Column(String, primary_key=True)
    school_id = Column(String, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(10))
    website = Column(String(500))
    
    # Programs stored as JSON array
    programs = Column(JSON)  # ["Toán học", "Khoa học máy tính", ...]
    
    school = relationship("School", back_populates="faculties")
