import json
import sys
from pathlib import Path
import glob

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from app.models import Base, School, Campus, Faculty


def import_schools_from_file(db, json_file: str):
    """Import schools from a single JSON file"""
    
    print(f"\n📄 Processing file: {json_file}")
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Support both formats
    if isinstance(data, dict) and 'schools' in data:
        # Format: {"schools": [...]}
        schools_data = data['schools']
    elif isinstance(data, list):
        # Format: [...]
        schools_data = data
    else:
        print(f"⚠️  Skipping {json_file}: Invalid format (expected array or object with 'schools' key)")
        return 0, 0, 0
    
    # Check if data is empty
    if not schools_data:
        print(f"   ℹ️  File is empty, skipping...")
        return 0, 0, 0
    
    schools_count = 0
    campuses_count = 0
    faculties_count = 0
    
    # Import schools
    for school_data in schools_data:
        try:
            print(f"   → Importing: {school_data['name']}")
            
            # Check if school already exists
            existing_school = db.query(School).filter(School.id == school_data['id']).first()
            if existing_school:
                print(f"      ⚠️  School '{school_data['id']}' already exists, skipping...")
                continue
            
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
            for campus_data in school_data.get('campuses', []):
                campus = Campus(
                    school_id=school_data['id'],
                    name=campus_data['name'],
                    address=campus_data['address'],
                    is_main=campus_data.get('is_main', False)
                )
                db.add(campus)
                campuses_count += 1
            
            # Create faculties
            for faculty_data in school_data.get('faculties', []):
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
            
        except KeyError as e:
            print(f"      ❌ Error: Missing required field {e} in school data")
            continue
        except Exception as e:
            print(f"      ❌ Error importing school: {e}")
            continue
    
    return schools_count, campuses_count, faculties_count


def import_all_schools(data_dir: str = "data"):
    """Import schools from all JSON files in data directory"""
    
    print("="*60)
    print("🎓 Schools API - Data Import")
    print("="*60)
    
    # Create tables
    print("\n📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Find all JSON files in data directory
    json_files = glob.glob(f"{data_dir}/*.json")
    
    if not json_files:
        print(f"\n⚠️  No JSON files found in '{data_dir}/' directory")
        return
    
    print(f"\n📁 Found {len(json_files)} JSON file(s) in '{data_dir}/':")
    for f in json_files:
        print(f"   - {f}")
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        print(f"\n🗑️  Clearing existing data...")
        db.query(Faculty).delete()
        db.query(Campus).delete()
        db.query(School).delete()
        db.commit()
        print("   ✅ Database cleared")
        
        total_schools = 0
        total_campuses = 0
        total_faculties = 0
        
        # Import from each JSON file
        for json_file in sorted(json_files):
            try:
                schools, campuses, faculties = import_schools_from_file(db, json_file)
                total_schools += schools
                total_campuses += campuses
                total_faculties += faculties
                
                if schools > 0:
                    print(f"   ✅ Imported {schools} schools, {campuses} campuses, {faculties} faculties")
                
            except json.JSONDecodeError as e:
                print(f"   ❌ Error: Invalid JSON in {json_file}: {e}")
                continue
            except Exception as e:
                print(f"   ❌ Error processing {json_file}: {e}")
                continue
        
        # Commit all changes
        db.commit()
        
        print("\n" + "="*60)
        if total_schools > 0:
            print("✅ Import completed successfully!")
            print(f"📊 Total imported:")
            print(f"   • {total_schools} schools")
            print(f"   • {total_campuses} campuses")
            print(f"   • {total_faculties} faculties")
        else:
            print("⚠️  No schools were imported")
            print("   Database is empty and ready for contributions!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Fatal error during import: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    import_all_schools()