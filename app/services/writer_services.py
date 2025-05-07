from app.models.writer import Writer
from app.models.article import Article
from app.services.user_services import create_user
from app import db
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import format_date, format_date_to_obj

def create_writer(username: Optional[str] = None, 
                  password: Optional[str] = None, 
                  email: Optional[str] = None, 
                  first_name: Optional[str] = None, 
                  last_name: Optional[str] = None, 
                  birth_date: Optional[str] = None,
                  phone_number: Optional[str] = None) -> Writer:
    """Create a new writer."""
    new_user = create_user(
        username=username,
        password=password, # Pass as plain text, will be hashed in user_services
        role="writer",
        email=email,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,  # LEAVE AS STRING, CONVERT IN USER SERVICES
        phone_number=phone_number
    )
    db.session.add(new_user)
    db.session.commit()

    # Create a new writer record
    new_writer = Writer(
        user=new_user
    )
    db.session.add(new_writer)
    db.session.commit()
    return new_writer

def update_writer(writer_id: int,
                     username: Optional[str] = None, 
                     password: Optional[str] = None, 
                     email: Optional[str] = None, 
                     first_name: Optional[str] = None, 
                     last_name: Optional[str] = None, 
                     birth_date: Optional[str] = None,
                     phone_number: Optional[str] = None) -> Writer:
     """Update a writer's information.
     All parameters are optional. Birth date should be in the format 'YYYY-MM-DD'.
     """
     writer = Writer.query.get(writer_id)
     if not writer:
          return None
     if username:
          writer.user.username = username
     if password:
          writer.user.password = generate_password_hash(password)
     if email:
          writer.user.email = email
     if first_name:
          writer.user.first_name = first_name
     if last_name:
          writer.user.last_name = last_name
     if birth_date:
          writer.user.birth_date = format_date_to_obj(birth_date)
          # Not a string this time, but a date object!
     if phone_number:
          writer.user.phone_number = phone_number
    
     db.session.commit()
     return writer

def get_all_authored_articles(writer_id: int) -> List[Article]:
    """Get all articles authored by a specific writer."""
    writer = Writer.query.get(writer_id)
    if not writer:
        return []
    return writer.articles 