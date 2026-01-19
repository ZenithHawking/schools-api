#!/usr/bin/env python3
"""
Script to import schools data from JSON file to database
Usage: python scripts/import_data.py
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from app.models import Base, School, Campus, Faculty


def import_schools(json_file: str = "data/schools.json"):
    """Import schools from JSON file"""
    
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Load JSON data
    print(f"Loading data from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(Faculty).delete()
        db.query(Campus).delete()
        db.query(School).delete()
        db.commit()
        
        schools_count = 0
        campuses_count = 0
        faculties_count = 0
        
        # Import schools
        for school_data in data['schools']:
            print(f"\nImporting school: {school_data['name']}")
            
            # Create school
            school = School(
                id=school_data['id'],
                code=school_data['code'],
                name=school_data['name'],
                logo_url=school_data.get('logo_url'),
                description=school_data['description'],
                type=school_data['type'],
                country=school_data['country'],
                contact=school_data['contact'],
                verified=school_data['metadata']['verified'],
                created_at=school_data['metadata']['created_at'],
                updated_at=school_data['metadata']['updated_at']
            )
            db.add(school)
            db.flush()
            schools_count += 1
            
            # Create campuses
            for campus_data in school_data['campuses']:
                campus = Campus(
                    school_id=school_data['id'],
                    name=campus_data['name'],
                    address=campus_data['address'],
                    is_main=campus_data.get('is_main', False)
                )
                db.add(campus)
                campuses_count += 1
            
            # Create faculties
            for faculty_data in school_data['faculties']:
                faculty = Faculty(
                    id=faculty_data['id'],
                    school_id=school_data['id'],
                    name=faculty_data['name'],
                    code=faculty_data.get('code'),
                    website=faculty_data.get('website'),
                    programs=faculty_data.get('programs', [])
                )
                db.add(faculty)
                faculties_count += 1
        
        # Commit all changes
        db.commit()
        
        print("\n" + "="*50)
        print("Import completed successfully!")
        print(f"✅ Imported {schools_count} schools")
        print(f"✅ Imported {campuses_count} campuses")
        print(f"✅ Imported {faculties_count} faculties")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    import_schools()
