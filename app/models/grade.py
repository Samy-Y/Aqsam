from app import db
from datetime import datetime, timezone

class Grade(db.Model):
    """Model for storing student grades."""
    __tablename__ = "grade"

    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    subject_id  = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    grade       = db.Column(db.Float,    nullable=False)
    date        = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    comment     = db.Column(db.String(250))

    student = db.relationship("Student", back_populates="grades")
    subject = db.relationship("Subject", back_populates="grades")

    def __repr__(self):
        return f"<Grade {self.grade} for student {self.student_id}>"
