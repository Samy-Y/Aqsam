from app import db
from flask_login import UserMixin
from datetime import date

class User(UserMixin, db.Model):
    """User model for the application.
    
    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        password (str): Password for the user (hashed).
        role (str): Role of the user (admin, teacher, student, writer).
        email (str): Unique email address for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        birth_date (date): Date of birth of the user.
        phone_number (str): Phone number of the user.
    """
    __tablename__ = "user"

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(150), unique=True, nullable=False)
    password    = db.Column(db.String(200), nullable=False)
    role        = db.Column(db.String(20), nullable=False)           # 'admin' | 'teacher' | 'student' | 'writer'
    email       = db.Column(db.String(150), unique=True, nullable=False)
    first_name  = db.Column(db.String(150), nullable=False)
    last_name   = db.Column(db.String(150), nullable=False)
    birth_date  = db.Column(db.Date,       nullable=False)
    phone_number= db.Column(db.String(20))

    # one‑to‑one relationships back‑refs (set uselist=False)
    student  = db.relationship("Student",  back_populates="user", uselist=False)
    teacher  = db.relationship("Teacher",  back_populates="user", uselist=False)
    writer   = db.relationship("Writer",   back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
