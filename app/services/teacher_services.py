from app.services.user_services import create_user, get_user_by_id, get_teacher_by_id
from app.models.teacher import Teacher
from app import db
from werkzeug.security import generate_password_hash
from typing import Optional, List

def create_teacher(username: str, 
                   password: str,
                   email: str, 
                   first_name: str, 
                   last_name: str, 
                   birth_date: str,
                   phone_number: str,
                   subjects: List = None,
                   classes: List = None) -> Teacher:
    """
    Create a new teacher.
    
    Args:
        username: Username for the teacher
        password: Password for the teacher
        email: Email address
        first_name: First name
        last_name: Last name
        birth_date: Birth date as a string
        phone_number: Phone number
        subjects: Optional list of Subject objects to associate with the teacher
        classes: Optional list of Class objects to associate with the teacher
        
    Returns:
        The newly created Teacher object
    """
    hashed_password = generate_password_hash(password)
    new_user = create_user(
        username=username,
        password=hashed_password,
        role="teacher",
        email=email,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,  # LEAVE AS STRING, CONVERT IN USER SERVICES
        phone_number=phone_number
    )
    db.session.add(new_user)
    db.session.commit()

    # Create a new teacher record
    new_teacher = Teacher(
        user=new_user
    )
    
    # Add subjects if provided
    if subjects:
        new_teacher.subjects = subjects
        
    # Add classes if provided
    if classes:
        new_teacher.classes = classes
        
    db.session.add(new_teacher)
    db.session.commit()
    return new_teacher

def update_teacher(teacher_id: int, **kwargs) -> Optional[Teacher]:
    """
    Update teacher information.
    
    Args:
        teacher_id: ID of the teacher to update
        **kwargs: Keyword arguments with fields to update
        
    Returns:
        Updated Teacher object if found, None otherwise
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        return None
    
    user = teacher.user
    
    # Update user fields if provided
    user_fields = ['username', 'email', 'first_name', 'last_name', 
                  'birth_date', 'phone_number']
    for field in user_fields:
        if field in kwargs:
            setattr(user, field, kwargs[field])
    
    # Update password if provided
    if 'password' in kwargs:
        user.password = generate_password_hash(kwargs['password'])
    
    db.session.commit()
    return teacher

def add_subject_to_teacher(teacher_id: int, subject) -> Optional[Teacher]:
    """
    Add a subject to a teacher.
    
    Args:
        teacher_id: ID of the teacher
        subject: Subject object to add
        
    Returns:
        Updated Teacher object if found, None otherwise
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher or subject in teacher.subjects:
        return teacher
    
    teacher.subjects.append(subject)
    db.session.commit()
    return teacher

def remove_subject_from_teacher(teacher_id: int, subject) -> Optional[Teacher]:
    """
    Remove a subject from a teacher.
    
    Args:
        teacher_id: ID of the teacher
        subject: Subject object to remove
        
    Returns:
        Updated Teacher object if found, None otherwise
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher or subject not in teacher.subjects:
        return teacher
    
    teacher.subjects.remove(subject)
    db.session.commit()
    return teacher

def add_class_to_teacher(teacher_id: int, class_obj) -> Optional[Teacher]:
    """
    Add a class to a teacher.
    
    Args:
        teacher_id: ID of the teacher
        class_obj: Class object to add
        
    Returns:
        Updated Teacher object if found, None otherwise
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher or class_obj in teacher.classes:
        return teacher
    
    teacher.classes.append(class_obj)
    db.session.commit()
    return teacher

def remove_class_from_teacher(teacher_id: int, class_obj) -> Optional[Teacher]:
    """
    Remove a class from a teacher.
    
    Args:
        teacher_id: ID of the teacher
        class_obj: Class object to remove
        
    Returns:
        Updated Teacher object if found, None otherwise
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher or class_obj not in teacher.classes:
        return teacher
    
    teacher.classes.remove(class_obj)
    db.session.commit()
    return teacher

def get_teachers_by_subject(subject) -> List[Teacher]:
    """
    Get all teachers associated with a specific subject.
    
    Args:
        subject: Subject object
        
    Returns:
        List of Teacher objects associated with the subject
    """
    return Teacher.query.filter(Teacher.subjects.contains(subject)).all()