from app import db
from app.models.teacher_junction import teacher_subject, teacher_class

class Teacher(db.Model):
    """Model for the Teacher entity.
    Attributes:
        id (int): The unique identifier for the teacher.
        subjects (list): A list of subjects associated with the teacher.
        classes (list): A list of classes associated with the teacher.
        grades (list): A list of grades associated with the teacher.
        user (User): The user associated with the teacher.
    Relationships:
        subjects (list): Many-to-many relationship with the Subject model.
        classes (list): Many-to-many relationship with the Class model.
        grades (list): One-to-many relationship with the Grade model.
        user (User): One-to-one relationship with the User model.
    """
    __tablename__ = "teachers"

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    # Many‑to‑many relationships
    subjects = db.relationship(
        "Subject",
        secondary=teacher_subject,
        back_populates="teachers",
    )

    classes = db.relationship(
        "Class",
        secondary=teacher_class,
        back_populates="teachers",
    )

    grades = db.relationship(
        "Grade",
        secondary="teacher_grades",
        back_populates="teacher",
    )


    user = db.relationship("User", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher {self.user.username}>"