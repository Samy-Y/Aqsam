# avoided python keyword :)
from app import db
from app.models.teacher_junction import teacher_class  # junction import

class Class(db.Model):
    __tablename__ = "class"

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(50), nullable=False)   # e.g. "1A"
    level = db.Column(db.String(50), nullable=False)   # e.g. "Grade 9"

    students = db.relationship("Student", back_populates="class_")
    teachers = db.relationship(
        "Teacher",
        secondary=teacher_class,
        back_populates="classes",
    )

    def __repr__(self):
        return f"<Class {self.name}>"
