from app import db
from app.models.teacher_junction import teacher_subject, teacher_class

class Teacher(db.Model):
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

    user = db.relationship("User", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher {self.user.username}>"