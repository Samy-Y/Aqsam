from app.models.grade import Grade
from app.models.subject import Subject
from app.models.student import Student
from app.models.teacher import Teacher
from app import db
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import func

def create_grade(student_id: int, subject_id: int, teacher_id: int, grade: float, comment: Optional[str] = None) -> Optional[Grade]:
    """
    Create a new grade for a student in a specific subject.
    
    Args:
        student_id: ID of the student
        subject_id: ID of the subject
        teacher_id: ID of the teacher assigning the grade
        grade: The grade value
        comment: Optional comment about the grade
        
    Returns:
        Created Grade object if successful, None otherwise
    """
    student = Student.query.get(student_id)
    subject = Subject.query.get(subject_id)
    teacher = Teacher.query.get(teacher_id)
    
    if not student or not subject or not teacher:
        return None
    
    new_grade = Grade(
        student_id=student.id,
        subject_id=subject.id,
        teacher_id=teacher.id,
        grade=grade,
        date=datetime.now(timezone.utc),
        comment=comment
    )
    
    db.session.add(new_grade)
    db.session.commit()
    
    return new_grade

def update_grade(grade_id: int, grade: Optional[float] = None, comment: Optional[str] = None) -> Optional[Grade]:
    """
    Update an existing grade.
    
    Args:
        grade_id: ID of the grade to update
        grade: New grade value
        comment: New comment about the grade
        
    Returns:
        Updated Grade object if found, None otherwise
    """
    grade_obj = Grade.query.get(grade_id)
    
    if not grade_obj:
        return None
    
    if grade is not None:
        grade_obj.grade = grade
    
    if comment is not None:
        grade_obj.comment = comment
    
    db.session.commit()
    
    return grade_obj

def delete_grade(grade_id: int) -> bool:
    """
    Delete a grade.
    
    Args:
        grade_id: ID of the grade to delete
        
    Returns:
        True if successful, False otherwise
    """
    grade_obj = Grade.query.get(grade_id)
    
    if not grade_obj:
        return False
    
    db.session.delete(grade_obj)
    db.session.commit()
    
    return True

def get_grade_by_id(grade_id: int) -> Optional[Grade]:
    """
    Get a grade by its ID.
    
    Args:
        grade_id: ID of the grade to retrieve
        
    Returns:
        Grade object if found, None otherwise
    """
    return Grade.query.get(grade_id)

def get_grades_by_student(student_id: int) -> List[Grade]:
    """
    Get all grades for a specific student.
    
    Args:
        student_id: ID of the student
        
    Returns:
        List of Grade objects for the student
    """
    return Grade.query.filter_by(student_id=student_id).all()

def get_grades_by_subject(subject_id: int) -> List[Grade]:
    """
    Get all grades for a specific subject.
    
    Args:
        subject_id: ID of the subject
        
    Returns:
        List of Grade objects for the subject
    """
    return Grade.query.filter_by(subject_id=subject_id).all()

def get_grades_by_teacher(teacher_id: int) -> List[Grade]:
    """
    Get all grades assigned by a specific teacher.
    
    Args:
        teacher_id: ID of the teacher
        
    Returns:
        List of Grade objects assigned by the teacher
    """
    return Grade.query.filter_by(teacher_id=teacher_id).all()

def get_grades_by_student_and_subject(student_id: int, subject_id: int) -> List[Grade]:
    """
    Get all grades for a student in a specific subject.
    
    Args:
        student_id: ID of the student
        subject_id: ID of the subject
        
    Returns:
        List of Grade objects for the student in the subject
    """
    return Grade.query.filter_by(student_id=student_id, subject_id=subject_id).all()

def get_average_grade_by_student(student_id: int) -> Optional[float]:
    """
    Get the average grade for a student across all subjects.
    
    Args:
        student_id: ID of the student
        
    Returns:
        Average grade as float if student has grades, None otherwise
    """
    result = db.session.query(func.avg(Grade.grade)).filter_by(student_id=student_id).scalar()
    return float(result) if result is not None else None

def get_average_grade_by_subject(subject_id: int) -> Optional[float]:
    """
    Get the average grade for a subject across all students.
    
    Args:
        subject_id: ID of the subject
        
    Returns:
        Average grade as float if subject has grades, None otherwise
    """
    result = db.session.query(func.avg(Grade.grade)).filter_by(subject_id=subject_id).scalar()
    return float(result) if result is not None else None

def get_student_subject_grades_summary(student_id: int) -> Dict[str, Any]:
    """
    Get a summary of grades for a student grouped by subject.
    
    Args:
        student_id: ID of the student
        
    Returns:
        Dictionary mapping subject names to average grades
    """
    grades = Grade.query.filter_by(student_id=student_id).all()
    summary = {}
    
    for grade in grades:
        subject_name = grade.subject.name
        if subject_name not in summary:
            summary[subject_name] = {
                'grades': [],
                'average': 0
            }
        
        summary[subject_name]['grades'].append(grade.grade)
    
    # Calculate averages
    for subject_name in summary:
        grades_list = summary[subject_name]['grades']
        summary[subject_name]['average'] = sum(grades_list) / len(grades_list)
    
    return summary

def get_recent_grades(limit: int = 10) -> List[Grade]:
    """
    Get the most recent grades.
    
    Args:
        limit: Maximum number of grades to return
        
    Returns:
        List of Grade objects sorted by date (newest first)
    """
    return Grade.query.order_by(Grade.date.desc()).limit(limit).all()