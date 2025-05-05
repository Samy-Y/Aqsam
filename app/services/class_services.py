from app.models.class_ import Class
from app.models.teacher import Teacher
from app import db
from typing import Optional, List

def create_class(name: str, level: str) -> Optional[Class]:
    """
    Create a new class.
    
    Args:
        name: Name of the class (e.g., "1A")
        level: Level of the class (e.g., "Grade 9")
        
    Returns:
        Created Class object if successful, None otherwise
    """
    if not name or not level:
        return None
    
    new_class = Class(name=name, level=level)
    db.session.add(new_class)
    db.session.commit()
    return new_class

def update_class(class_id: int, name: Optional[str] = None, level: Optional[str] = None) -> Optional[Class]:
    """
    Update a class's information.
    
    Args:
        class_id: ID of the class to update
        name: New name for the class
        level: New level for the class
        
    Returns:
        Updated Class object if found, None otherwise
    """
    class_obj = get_class_by_id(class_id)
    if not class_obj:
        return None
    
    if name:
        class_obj.name = name
    if level:
        class_obj.level = level
    
    db.session.commit()
    return class_obj

def delete_class(class_id: int) -> bool:
    """
    Delete a class.
    
    Args:
        class_id: ID of the class to delete
        
    Returns:
        True if successful, False otherwise
    """
    class_obj = get_class_by_id(class_id)
    if not class_obj:
        return False
    
    db.session.delete(class_obj)
    db.session.commit()
    return True

def get_class_by_id(class_id: int) -> Optional[Class]:
    """
    Get a class by its ID.
    
    Args:
        class_id: ID of the class
        
    Returns:
        Class object if found, None otherwise
    """
    return Class.query.get(class_id)

def get_class_by_name(name: str) -> Optional[Class]:
    """
    Get a class by its name.
    
    Args:
        name: Name of the class
        
    Returns:
        Class object if found, None otherwise
    """
    return Class.query.filter_by(name=name).first()

def get_classes_by_level(level: str) -> List[Class]:
    """
    Get all classes at a specific level.
    
    Args:
        level: Level of the classes to retrieve
        
    Returns:
        List of Class objects at the specified level
    """
    return Class.query.filter_by(level=level).all()

def get_all_classes() -> List[Class]:
    """
    Get all classes.
    
    Returns:
        List of all Class objects
    """
    return Class.query.all()

def add_teacher_to_class(class_id: int, teacher_id: int) -> Optional[Class]:
    """
    Add a teacher to a class.
    
    Args:
        class_id: ID of the class
        teacher_id: ID of the teacher
        
    Returns:
        Updated Class object if successful, None otherwise
    """
    class_obj = get_class_by_id(class_id)
    teacher = Teacher.query.get(teacher_id)
    
    if not class_obj or not teacher:
        return None
    
    if teacher not in class_obj.teachers:
        class_obj.teachers.append(teacher)
        db.session.commit()
    
    return class_obj

def remove_teacher_from_class(class_id: int, teacher_id: int) -> Optional[Class]:
    """
    Remove a teacher from a class.
    
    Args:
        class_id: ID of the class
        teacher_id: ID of the teacher
        
    Returns:
        Updated Class object if successful, None otherwise
    """
    class_obj = get_class_by_id(class_id)
    teacher = Teacher.query.get(teacher_id)
    
    if not class_obj or not teacher:
        return None
    
    if teacher in class_obj.teachers:
        class_obj.teachers.remove(teacher)
        db.session.commit()
    
    return class_obj

def get_classes_by_teacher(teacher_id: int) -> List[Class]:
    """
    Get all classes taught by a specific teacher.
    
    Args:
        teacher_id: ID of the teacher
        
    Returns:
        List of Class objects taught by the teacher
    """
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return []
    
    return teacher.classes

def get_student_count_in_class(class_id: int) -> int:
    """
    Get the number of students in a class.
    
    Args:
        class_id: ID of the class
        
    Returns:
        Number of students in the class
    """
    class_obj = get_class_by_id(class_id)
    if not class_obj:
        return 0
    
    return len(class_obj.students)
