from app.models.student import Student
from app.services.user_services import create_user
from app import db
from werkzeug.security import generate_password_hash
from typing import Optional, List
from app.utils import format_date, format_date_to_obj

def create_student(username: str, 
                   password: str,
                   email: str, 
                   first_name: str, 
                   last_name: str, 
                   birth_date: str,
                   phone_number: str,
                   class_id: Optional[int] = None) -> Student:
                    # i cannot believe there isn't a easier way than Optional[int] = None
    """Create a new student."""
    new_user = create_user(
        username=username,
        password=password, # Will be hashed in create_user
        role="student",
        email=email,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date, # LEAVE AS STRING, CONVERT IN USER SERVICES
        phone_number=phone_number
    )
    db.session.add(new_user)
    db.session.commit()

    # Create a new student record
    new_student = Student(
        user=new_user,
        class_id=class_id
    )
    db.session.add(new_student)
    db.session.commit()
    return new_student

def update_student(student_id: int, 
                   username: Optional[str] = None, 
                   password: Optional[str] = None, 
                   email: Optional[str] = None, 
                   first_name: Optional[str] = None, 
                   last_name: Optional[str] = None, 
                   birth_date: Optional[str] = None,
                   phone_number: Optional[str] = None,
                   class_id: Optional[int] = None) -> Student:
    """Update a student's information.
    All parameters are optional. Birth date should be in the format 'YYYY-MM-DD'.
    Password will be hashed. Pass as plaintext.
    """
    student = Student.query.get(student_id)
    if not student:
        return None
    if username:
        student.user.username = username
    if password:
        student.user.password = generate_password_hash(password)
    if email:
        student.user.email = email
    if first_name:
        student.user.first_name = first_name
    if last_name:
        student.user.last_name = last_name
    if birth_date:
        student.user.birth_date = format_date_to_obj(birth_date)
    if phone_number:
        student.user.phone_number = phone_number
    if class_id:
        student_obj = Student.query.get(student_id)
        student_obj.class_id = class_id
    db.session.commit()
    return student
    
def get_all_student_by_class_id(class_id: int) -> List[Student]:
    """Get all students in a specific class."""
    return Student.query.filter_by(class_id=class_id).all()

def get_student_by_id(student_id: int) -> Optional[Student]:
    """Get a student by their User-ID."""
    return Student.query.get(student_id)

def get_student_class_id_by_id(student_id: int) -> Optional[int]:
    """Get the class ID of a student by their ID."""
    student = get_student_by_id(student_id)
    if student:
        return student.class_id if student.class_id else None
    return None