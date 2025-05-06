from app.services.user_services import create_user, get_user_by_id, get_teacher_by_id
from app.models.teacher import Teacher
from app.models.subject import Subject
from app.models.class_ import Class
from app import db
from werkzeug.security import generate_password_hash
from typing import Optional, List

def create_teacher(username: str, 
                   password: str, # Plain password
                   email: str, 
                   first_name: str, 
                   last_name: str, 
                   birth_date: str,
                   phone_number: str,
                   subjects_ids: List[int] = None, # Changed from subjects to subjects_ids
                   classes_ids: List[int] = None,  # Changed from classes to classes_ids
                   activated: bool = True
                   ) -> Optional[Teacher]:
    """
    Create a new teacher.
    
    Args:
        username: Username for the teacher
        password: Plain password for the teacher
        email: Email address
        first_name: First name
        last_name: Last name
        birth_date: Birth date as a string 'YYYY-MM-DD'
        phone_number: Phone number
        subjects_ids: Optional list of Subject IDs to associate with the teacher
        classes_ids: Optional list of Class IDs to associate with the teacher
        activated: Activation status for the user
        
    Returns:
        The newly created Teacher object or None if user creation failed
    """
    # User is created first
    new_user = create_user(
        username=username,
        password=password, # Pass plain password, create_user will hash it
        role="teacher",
        email=email,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        phone_number=phone_number
    )
    if not new_user:
        return None
    
    new_user.activated = activated # Set activation status for user

    # Create a new teacher record
    new_teacher = Teacher(user_id=new_user.id) # Link by user_id
    db.session.add(new_teacher)

    # Add subjects if provided
    if subjects_ids:
        teacher_subjects = Subject.query.filter(Subject.id.in_(subjects_ids)).all()
        new_teacher.subjects = teacher_subjects
        
    # Add classes if provided
    if classes_ids:
        teacher_classes = Class.query.filter(Class.id.in_(classes_ids)).all()
        new_teacher.classes = teacher_classes
        
    db.session.commit() # Commit once after all associations
    return new_teacher

def update_teacher(teacher_id: int, **kwargs) -> Optional[Teacher]:
    """
    Update teacher information.
    
    Args:
        teacher_id: ID of the teacher to update
        **kwargs: Keyword arguments with fields to update. 
                  Includes 'subjects_ids' and 'classes_ids' as lists of IDs.
        
    Returns:
        Updated Teacher object if found, None otherwise
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        return None
    
    user = teacher.user
    
    # Update user fields if provided
    user_fields = ['username', 'email', 'first_name', 'last_name', 
                   'birth_date', 'phone_number', 'activated']
    for field in user_fields:
        if field in kwargs and kwargs[field] is not None:
            setattr(user, field, kwargs[field])
            if field == 'birth_date' and kwargs[field]: # Ensure birth_date is converted if string
                from app.utils import format_date_to_obj
                user.birth_date = format_date_to_obj(kwargs[field])


    # Update password if provided and not empty
    if 'password' in kwargs and kwargs['password']:
        user.password = generate_password_hash(kwargs['password'])

    # Update subjects
    if 'subjects_id' in kwargs: # Note: form field is subjects_id, passed as subjects_id
        subjects_ids = kwargs['subjects_id']
        if subjects_ids is not None: # Check if it's explicitly provided (could be empty list)
            teacher_subjects = Subject.query.filter(Subject.id.in_(subjects_ids)).all()
            teacher.subjects = teacher_subjects
        else: # If None, perhaps means no change or clear them
            teacher.subjects = []


    # Update classes
    if 'classes_id' in kwargs: # Note: form field is classes_id, passed as classes_id
        classes_ids = kwargs['classes_id']
        if classes_ids is not None:
            teacher_classes = Class.query.filter(Class.id.in_(classes_ids)).all()
            teacher.classes = teacher_classes
        else:
            teacher.classes = []
            
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