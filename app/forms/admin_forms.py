from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField, SelectField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from flask_wtf.file import FileAllowed
from wtforms.widgets import TextArea
from app.models.user import User
from app import db
from app.services.class_services import get_class_by_id, get_all_classes, get_class_by_name
from app.services.subject_services import get_all_subjects, get_subject_by_name
from app.models.teacher import Teacher
import re

# User-Related Forms

class CreateUserForm(FlaskForm):
    """Form for creating a new user."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[("student","Student"),
                                        ("teacher","Teacher"),
                                        ("writer","Writer"),
                                        ("admin", "Admin")],
                                validators=[DataRequired()])
    email = StringField('Email')
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number')
    activated = BooleanField('Activated')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data:
            # regex code to check email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Invalid email format. Please enter a valid email address.')
        # Check if email already exists in the database
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')
        return True
        
    def validate_role(self, role):
        if role.data not in ['admin', 'teacher', 'student', 'writer']:
            raise ValidationError('Invalid role. Must be one of: admin, teacher, student, writer.')

class DeleteUserForm(FlaskForm):
    """Form for deleting a user."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Delete User')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('That username does not exist. Please choose a different one.')

class ChangeUserProfilePictureForm(FlaskForm):
    """Form for changing a user's profile picture through a file upload."""
    
    user_id = StringField('User ID', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif', 'heic'], 'Images only!')])
    submit = SubmitField('Change Profile Picture')

    def validate_profile_picture(self, profile_picture):
        if not profile_picture.data:
            raise ValidationError('No file selected. Please choose a file to upload.')

# Class/Level-Related Forms

class CreateClassForm(FlaskForm):
    """Form for creating a new class."""
    
    name = StringField('Class Name', validators=[DataRequired(), Length(min=1, max=50)])
    level = StringField('Level', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create Class')

    def validate_name(self, name):
        existing_class = get_class_by_name(name.data)
        if existing_class:
            if existing_class.level == self.level.data:
                raise ValidationError('A class with this name in the same level already exists.')

class UpdateClassForm(FlaskForm):
    """Form for updating an existing class."""
    
    name = StringField('Class Name', validators=[DataRequired(), Length(min=1, max=50)])
    level = StringField('Level', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Update Class')

    def validate_name(self, name):
        from app.services.class_services import get_class_by_name
        existing_class = get_class_by_name(name.data)
        if existing_class and existing_class.level == self.level.data:
                raise ValidationError('A class with this name in the same level already exists.')

class DeleteClassForm(FlaskForm):
    """Form for deleting a class."""
    
    confirm_delete = BooleanField('I confirm I want to delete this class', validators=[DataRequired()])
    submit = SubmitField('Delete Class')

class AssignTeacherForm(FlaskForm):
    """Form for assigning a teacher to a class."""
    
    class_id = SelectField('Class', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Teacher')

    def __init__(self, *args, **kwargs):
        super(AssignTeacherForm, self).__init__(*args, **kwargs)
        
        # Populate class choices
        classes = get_all_classes()
        self.class_id.choices = [(c.id, f"{c.name} - {c.level}") for c in classes]

class RemoveTeacherForm(FlaskForm):
    """Form for removing a teacher from a class."""
    
    class_id = SelectField('Class', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Remove Teacher')
    
    def __init__(self, *args, **kwargs):
        super(RemoveTeacherForm, self).__init__(*args, **kwargs)
        
        # Populate class choices
        classes = get_all_classes()
        self.class_id.choices = [(c.id, f"{c.name} - {c.level}") for c in classes]
        
        # Initially set empty teacher choices - these will be populated via AJAX based on class selection
        self.teacher_id.choices = []

class ClassFilterForm(FlaskForm):
    """Form for filtering classes by level."""
    
    level = SelectField('Filter by Level', validators=[])
    submit = SubmitField('Filter')
    
    def __init__(self, *args, **kwargs):
        super(ClassFilterForm, self).__init__(*args, **kwargs)
        from app.models.class_ import Class
        
        # Get unique levels for filtering
        levels = db.session.query(Class.level).distinct().all()
        self.level.choices = [("", "All Levels")] + [(level[0], level[0]) for level in levels]

# Student-Related Forms

class CreateStudentForm(FlaskForm):
    """Form for creating a new student."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email')
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField('Date of Birth', format='%Y-%m-%d')
    phone_number = StringField('Phone Number')
    class_id = SelectField('Class', coerce=int)
    submit = SubmitField('Create Student')

    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        self.class_id.choices = [(c.id, f"{c.name} - {c.level}") for c in get_all_classes()]
        self.class_id.choices.insert(0, (0, "Select Class"))  # Add a default option

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data:
            # regex code to check email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Invalid email format. Please enter a valid email address.')
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')
        return True
        
    def validate_class_id(self, class_id):
        if class_id.data == 0:
            raise ValidationError('Please select a class.')
        class_ = get_class_by_id(class_id.data)
        if not class_:
            raise ValidationError('That class does not exist. Please choose a different one.')
        
class UpdateStudentForm(FlaskForm):
    """Form for updating an existing student."""
    
    original_username = StringField('Hidden Username', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password')
    email = StringField('Email')
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField('Date of Birth', format='%Y-%m-%d')
    phone_number = StringField('Phone Number')
    class_id = SelectField('Class', coerce=int)
    submit = SubmitField('Update Student')

    def __init__(self, *args, **kwargs):
        super(UpdateStudentForm, self).__init__(*args, **kwargs)
        
        # Populate class choices
        classes = get_all_classes()
        self.class_id.choices = [(c.id, f"{c.name} - {c.level}") for c in classes]

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and username.data != self.original_username.data:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and email.data:
            raise ValidationError('That email is already registered. Please choose a different one.')
    
    def validate_class_id(self, class_id):
        class_ = get_class_by_id(class_id.data)
        if not class_:
            raise ValidationError('That class does not exist. Please choose a different one.')

# Teacher-Related Forms

class CreateTeacherForm(FlaskForm):
    """Form for creating a new teacher."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email')
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    classes_id = SelectMultipleField('Classes', coerce=int, validators=[DataRequired()])
    subjects_id = SelectMultipleField('Subjects', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Teacher')

    def __init__(self, *args, **kwargs):
        super(CreateTeacherForm, self).__init__(*args, **kwargs)
        self.classes_id.choices = [(c.id, f"{c.name} - {c.level}") for c in get_all_classes()]
        self.subjects_id.choices = [(s.id, s.name) for s in get_all_subjects()]

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data:
            # regex code to check email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Invalid email format. Please enter a valid email address.')
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')
        return True

class UpdateTeacherForm(FlaskForm):
    """Form for updating an existing teacher."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[Length(min=6)])
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    classes_id = SelectMultipleField('Classes', coerce=int)
    subjects_id = SelectMultipleField('Subjects', coerce=int)
    submit = SubmitField('Update Teacher')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UpdateTeacherForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.classes_id.choices = [(c.id, f"{c.name} - {c.level}") for c in get_all_classes()]
        self.subjects_id.choices = [(s.id, s.name) for s in get_all_subjects()]

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data and email.data != self.original_email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Invalid email format. Please enter a valid email address.')
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')
        return True
    
# Article-Related Forms
class CreateWriterForm(FlaskForm):
    """Form for creating a new writer."""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email')
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number')
    activated = BooleanField('Activated', default=True)
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    submit = SubmitField('Create Writer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Invalid email format. Please enter a valid email address.')
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')
        return True

class UpdateWriterForm(FlaskForm):
    """Form for updating an existing writer."""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[Length(min=6)]) 
    email = StringField('Email') 
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number') 
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d') 
    activated = BooleanField('Activated')
    submit = SubmitField('Update Writer')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UpdateWriterForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data and email.data != self.original_email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Invalid email format. Please enter a valid email address.')
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')
        return True

class CreateArticleForm(FlaskForm):
    """Form for creating a new article."""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    content_md = StringField('Content (Markdown)', widget=TextArea(), validators=[DataRequired()]) # Using StringField with TextArea widget
    is_published = BooleanField('Publish Immediately?', default=False)
    submit = SubmitField('Create Article')

    def __init__(self, *args, **kwargs):
        super(CreateArticleForm, self).__init__(*args, **kwargs)
        # Populate author choices with users who are writers
        writers = User.query.filter_by(role='writer').all()
        self.author_id.choices = [(writer.id, writer.username) for writer in writers]
        if not self.author_id.choices:
            self.author_id.choices = [(0, "No writers available - create a writer first")]


class UpdateArticleForm(FlaskForm):
    """Form for updating an existing article."""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    content_md = StringField('Content (Markdown)', widget=TextArea(), validators=[DataRequired()]) # Using StringField with TextArea widget
    is_published = BooleanField('Is Published?')
    submit = SubmitField('Update Article')

    def __init__(self, *args, **kwargs):
        super(UpdateArticleForm, self).__init__(*args, **kwargs)
        writers = User.query.filter_by(role='writer').all()
        self.author_id.choices = [(writer.id, writer.username) for writer in writers]
        if not self.author_id.choices:
            self.author_id.choices = [(0, "No writers available")]


class DeleteArticleForm(FlaskForm):
    """Form for deleting an article."""
    confirm_delete = BooleanField('I confirm I want to delete this article', validators=[DataRequired()])
    submit = SubmitField('Delete Article')


# Subject Management Forms
class CreateSubjectForm(FlaskForm):
    """Form for creating a new subject."""
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Create Subject')

    def validate_name(self, name):
        subject = get_subject_by_name(name.data)
        if subject:
            raise ValidationError('That subject name already exists. Please choose a different one.')

class UpdateSubjectForm(FlaskForm):
    """Form for updating an existing subject."""
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update Subject')

    def __init__(self, original_name=None, *args, **kwargs):
        super(UpdateSubjectForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            subject = get_subject_by_name(name.data)
            if subject:
                raise ValidationError('That subject name '+ name.data +' already exists. Please choose a different one.')

class DeleteSubjectForm(FlaskForm):
    """Form for deleting a subject."""
    confirm_delete = BooleanField('I confirm I want to delete this subject', validators=[DataRequired()])
    submit = SubmitField('Delete Subject')