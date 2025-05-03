from app import db
from flask_login import UserMixin
from datetime import date

class User(UserMixin, db.Model):
    """User model for the application.
    
    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        password (str): Password for the user (hashed).
        role (str): Role of the user (admin, teacher, student, writer) (Must be lowercase!).
        email (str): Unique email address for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        birth_date (date): Date of birth of the user.
        phone_number (str): Phone number of the user.
        profile_picture_filename (str): URL to the user's profile picture. (in assets/profile_pictures/)
        email_verified (bool): Indicates if the user's email is verified.
        email_verification_token (str): Token for email verification.
        email_verification_expiry (datetime): Expiry time for the email verification token.
        password_reset_token (str): Token for password reset.
        password_reset_expiry (datetime): Expiry time for the password reset token.
        activated (bool): Indicates if the user's account is activated.
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
    email_verified            = db.Column(db.Boolean, default=False)         # Email verification status
    email_verification_token  = db.Column(db.String(200))         # Token for email verification
    email_verification_expiry = db.Column(db.DateTime)          # Expiry time for email verification token
    password_reset_token      = db.Column(db.String(200))            # Token for password reset
    password_reset_expiry     = db.Column(db.DateTime)             # Expiry time for password reset token
    activated   = db.Column(db.Boolean, default=False)             # Account activation status

    # one‑to‑one relationships back‑refs (set uselist=False)
    student  = db.relationship("Student",  back_populates="user", uselist=False)
    teacher  = db.relationship("Teacher",  back_populates="user", uselist=False)
    writer   = db.relationship("Writer",   back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
