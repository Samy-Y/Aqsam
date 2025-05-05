from app import db
from datetime import datetime, timezone

class Grade(db.Model):
    """Model for storing student grades.
    Attributes:
        id (int): Unique identifier for the grade.
        student_id (int): Foreign key referencing the student.
        subject_id (int): Foreign key referencing the subject.
        teacher_id (int): Foreign key referencing the teacher.
        grade (float): The grade value.
        date (datetime): The date when the grade was assigned.
        comment (str): Optional comment about the grade.
    Relationships:
        student (Student): The student associated with the grade.
        subject (Subject): The subject associated with the grade.
    """
    __tablename__ = "grade"

    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    subject_id  = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    teacher_id  = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False)
    grade       = db.Column(db.Float,    nullable=False)
    date        = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    comment     = db.Column(db.String(250))

    student = db.relationship("Student", back_populates="grades")
    subject = db.relationship("Subject", back_populates="grades")
    teacher = db.relationship("Teacher", secondary="teacher_grades", back_populates="grades")

    def __repr__(self):
        return f"<Grade {self.grade} for student {self.student_id}>"
