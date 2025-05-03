from app import db
from datetime import datetime

class Student(db.Model):
    """Model for storing student information.
    
    Attributes:
        id (int): Unique identifier for the student (foreign key to User).
        class_id (int): Identifier for the class the student is enrolled in (foreign key to Class).
        user (User): Relationship to the User model, representing the student.
    """
    __tablename__ = "student"

    id        = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    class_id  = db.Column(db.Integer, db.ForeignKey("class.id"))

    user    = db.relationship("User",   back_populates="student")
    class_  = db.relationship("Class",  back_populates="students")
    grades  = db.relationship("Grade",  back_populates="student")

    def __repr__(self):
        return f"<Student {self.user.username}>"
