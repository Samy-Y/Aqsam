from app import db
from app.models.teacher_junction import teacher_subject

class Subject(db.Model):
    """Model for the Subject entity.
    Attributes:
        id (int): The unique identifier for the subject.
        name (str): The name of the subject."""
    __tablename__ = "subject"

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    teachers = db.relationship(
        "Teacher",
        secondary=teacher_subject,
        back_populates="subjects",
    )
    grades = db.relationship("Grade", back_populates="subject")

    def __repr__(self):
        return f"<Subject {self.name}>"