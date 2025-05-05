from app.models.subject import Subject
from app import db
from typing import Optional

def create_subject(name: str) -> Optional[Subject]:
    """
    Create a new subject.
    
    Args:
        name: Name of the subject
        
    Returns:
        Created Subject object if successful, None otherwise
    """
    if not name:
        return None
    
    subject = Subject(name=name)
    db.session.add(subject)
    db.session.commit()
    return subject

def update_subject(subject_id: int, name: Optional[str] = None) -> Optional[Subject]:
    """
    Update a subject's information.
    
    Args:
        subject_id: ID of the subject to update
        name: New name for the subject
        
    Returns:
        Updated Subject object if found, None otherwise
    """
    subject = Subject.query.get(subject_id)
    if not subject:
        return None
    
    if name:
        subject.name = name
    
    db.session.commit()
    return subject

def delete_subject(subject_id: int) -> bool:
    """
    Delete a subject.
    
    Args:
        subject_id: ID of the subject to delete
        
    Returns:
        True if successful, False otherwise
    """
    subject = Subject.query.get(subject_id)
    if not subject:
        return False
    
    db.session.delete(subject)
    db.session.commit()
    return True

def get_subject_by_id(subject_id: int) -> Optional[Subject]:
    """
    Get a subject by its ID.
    
    Args:
        subject_id: ID of the subject
        
    Returns:
        Subject object if found, None otherwise
    """
    return Subject.query.get(subject_id)

def get_subject_by_name(name: str) -> Optional[Subject]:
    """
    Get a subject by its name.
    
    Args:
        name: Name of the subject
        
    Returns:
        Subject object if found, None otherwise
    """
    return Subject.query.filter_by(name=name).first()