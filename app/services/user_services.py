from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.writer import Writer
from app import db
from werkzeug.security import generate_password_hash
from typing import Optional, List
from datetime import datetime, timedelta
import secrets
from app.utils import format_date, format_date_to_obj

def get_user_by_id(user_id: int) -> Optional[User]:
    """Get a user by their ID."""
    return User.query.get(user_id)

def get_student_by_id(student_id: int) -> Optional[Student]:
    """Get a student by their ID."""
    return Student.query.get(student_id)

def get_teacher_by_id(teacher_id: int) -> Optional[Teacher]:
    """Get a teacher by their ID."""
    return Teacher.query.get(teacher_id)

def get_writer_by_id(writer_id: int) -> Optional[Writer]:
    """Get a writer by their ID."""
    return Writer.query.get(writer_id)

def get_user_by_email(email: str) -> Optional[User]:
    """Get a user by their email."""
    return User.query.filter_by(email=email).first()

def get_user_by_username(username: str) -> Optional[User]:
    """Get a user by their username."""
    return User.query.filter_by(username=username).first()

def get_users_by_role(role: str) -> List[User]:
    """Get all users with a specific role."""
    return User.query.filter_by(role=role).all()

def delete_user(user: User) -> bool:
    """Soft delete a user by setting activated to False."""
    user.activated = False
    db.session.commit()
    return True

def generate_email_verification_token(user: User, expiry_hours: int = 24) -> str:
    """Generate an email verification token for a user.
    
    Args:
        user: The user to generate a token for
        expiry_hours: Number of hours until token expires
        
    Returns:
        The generated token
    """
    token = secrets.token_urlsafe(32)  # Generate a secure random token
    user.email_verification_token = token
    user.email_verification_expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
    db.session.commit()
    return token

def verify_email(token: str) -> Optional[User]:
    """Verify a user's email using a token.
    
    Args:
        token: The verification token
        
    Returns:
        The user if verification was successful, None otherwise
    """
    user = User.query.filter_by(email_verification_token=token).first()
    
    if not user:
        return None
        
    # Check if token is expired
    if not user.email_verification_expiry or user.email_verification_expiry < datetime.utcnow():
        return None
    
    # Mark email as verified
    user.email_verified = True
    user.email_verification_token = None  # Clear the token
    user.email_verification_expiry = None  # Clear the expiry date
    db.session.commit()
    return user

def generate_password_reset_token(user: User, expiry_hours: int = 1) -> str:
    """Generate a password reset token for a user.
    
    Args:
        user: The user to generate a token for
        expiry_hours: Number of hours until token expires
        
    Returns:
        The generated token
    """
    token = secrets.token_urlsafe(32)  # Generate a secure random token
    user.password_reset_token = token
    user.password_reset_expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
    db.session.commit()
    return token

def reset_password(token: str, new_password: str) -> Optional[User]:
    """Reset a user's password using a token.
    
    Args:
        token: The password reset token
        new_password: The new password to set
        
    Returns:
        The user if reset was successful, None otherwise
    """
    user = User.query.filter_by(password_reset_token=token).first()
    
    if not user:
        return None
        
    # Check if token is expired
    if not user.password_reset_expiry or user.password_reset_expiry < datetime.utcnow():
        return None
    
    # Set new password
    user.password = generate_password_hash(new_password)
    user.password_reset_token = None  # Clear the token
    user.password_reset_expiry = None  # Clear the expiry date
    db.session.commit()
    return user

def activate_user(user: User) -> bool:
    """Activate a user account.
    
    Args:
        user: The user to activate
        
    Returns:
        True if successful
    """
    user.activated = True
    db.session.commit()
    return True

def deactivate_user(user: User) -> bool:
    """Deactivate a user account.
    
    Args:
        user: The user to deactivate
        
    Returns:
        True if successful
    """
    user.activated = False
    db.session.commit()
    return True

def is_account_active(user: User) -> bool:
    """Check if a user account is active.
    
    Args:
        user: The user to check
        
    Returns:
        True if the account is active
    """
    return user.activated

def create_user(username: str, password: str, role: str, email: Optional[str] = None, 
                first_name: Optional[str] = None, last_name: Optional[str] = None, birth_date: Optional[str] = None, 
                phone_number: Optional[str] = None) -> User:
    """Create a new user.
    
    Args:
        username: The username for the new user
        password: The password for the new user (will be hashed)
        role: The role for the new user
        email: The email address for the new user
        first_name: The first name of the new user
        last_name: The last name of the new user
        birth_date: The birth date of the new user (in 'YYYY-MM-DD' format)
        phone_number: The phone number of the new user (optional)
        
    Returns:
        The newly created user
    """
    hashed_password = generate_password_hash(password)
    
    user = User(
        username=username,
        password=hashed_password,
        role=role,
        email=email,
        first_name=first_name,
        last_name=last_name,
        birth_date=format_date_to_obj(birth_date),
        phone_number=phone_number,
        email_verified=False,  # Set to False by default
        email_verification_token=None,
        email_verification_expiry=None,
        password_reset_token=None,
        password_reset_expiry=None,
        activated=True  # Activate by default, can be changed as needed
    )
    
    db.session.add(user)
    db.session.commit()
    return user

def set_user_pfp(user_id: int, pfp_filename: str) -> bool:
    """Set the profile picture filename for a user.
    
    Args:
        user_id: The ID of the user
        pfp_filename: The filename of the profile picture
        
    Returns:
        True if successful
    """
    user = User.query.get(user_id)
    if not user:
        return False
    
    user.profile_picture_filename = pfp_filename
    db.session.commit()
    return True