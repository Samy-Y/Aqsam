from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User
from app import db
from typing import Optional
from app.services.class_services import get_class_by_id, get_all_classes
from app.services.subject_services import get_all_subjects
import re

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

# Class/Level-Related Forms

class CreateClassForm(FlaskForm):
    """Form for creating a new class."""
    
    name = StringField('Class Name', validators=[DataRequired(), Length(min=1, max=50)])
    level = StringField('Level', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create Class')

    def validate_name(self, name):
        from app.services.class_services import get_class_by_name
        existing_class = get_class_by_name(name.data)
        if existing_class:
            raise ValidationError('A class with this name already exists.')

class UpdateClassForm(FlaskForm):
    """Form for updating an existing class."""
    
    name = StringField('Class Name', validators=[DataRequired(), Length(min=1, max=50)])
    level = StringField('Level', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Update Class')

    def validate_name(self, name):
        from app.services.class_services import get_class_by_name
        existing_class = get_class_by_name(name.data)
        if existing_class and (not hasattr(self, '_original_obj') or self._original_obj.name != name.data):
            raise ValidationError('A class with this name already exists.')

class DeleteClassForm(FlaskForm):
    """Form for deleting a class."""
    
    confirm_delete = BooleanField('I confirm I want to delete this class', validators=[DataRequired()])
    submit = SubmitField('Delete Class')

class AssignTeacherForm(FlaskForm):
    """Form for assigning a teacher to a class."""
    
    class_id = SelectField('Class', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Teacher')

    def __init__(self, *args, **kwargs):
        super(AssignTeacherForm, self).__init__(*args, **kwargs)
        from app.services.class_services import get_all_classes
        from app.models.teacher import Teacher
        
        # Populate class choices
        classes = get_all_classes()
        self.class_id.choices = [(c.id, f"{c.name} - {c.level}") for c in classes]
        
        # Populate teacher choices
        teachers = Teacher.query.all()
        self.teacher_id.choices = [(t.id, f"{t.user.first_name} {t.user.last_name}") for t in teachers]

class RemoveTeacherForm(FlaskForm):
    """Form for removing a teacher from a class."""
    
    class_id = SelectField('Class', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Remove Teacher')
    
    def __init__(self, *args, **kwargs):
        super(RemoveTeacherForm, self).__init__(*args, **kwargs)
        from app.services.class_services import get_all_classes
        from app.models.teacher import Teacher
        
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

class CreateStudent(FlaskForm):
    """Form for creating a new student."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField('Date of Birth', format='%Y-%m-%d')
    phone_number = StringField('Phone Number')
    class_id = SelectField('Class', coerce=int)
    submit = SubmitField('Create Student')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')
        
    def validate_class_id(self, class_id):
        from app.services.class_services import get_class_by_id
        class_ = get_class_by_id(class_id.data)
        if not class_:
            raise ValidationError('That class does not exist. Please choose a different one.')
        
class UpdateStudent(FlaskForm):
    """Form for updating an existing student."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField('Date of Birth', format='%Y-%m-%d')
    phone_number = StringField('Phone Number')
    class_id = SelectField('Class', coerce=int)
    submit = SubmitField('Update Student')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')
    def validate_class_id(self, class_id):
        class_ = get_class_by_id(class_id.data)
        if not class_:
            raise ValidationError('That class does not exist. Please choose a different one.')
        
# Teacher-Related Forms

class CreateTeacher(FlaskForm):
    """Form for creating a new teacher."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    classes_id = SelectMultipleField('Classes', coerce=int, validators=[DataRequired()])
    subjects_id = SelectMultipleField('Subjects', coerce=int, validators=[DataRequired()])
    activated = BooleanField('Activated', default=True)
    submit = SubmitField('Create Teacher')

    def __init__(self, *args, **kwargs):
        super(CreateTeacher, self).__init__(*args, **kwargs)
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

class UpdateTeacher(FlaskForm):
    """Form for updating an existing teacher."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    classes_id = SelectMultipleField('Classes', coerce=int)
    subjects_id = SelectMultipleField('Subjects', coerce=int)
    activated = BooleanField('Activated')
    submit = SubmitField('Update Teacher')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UpdateTeacher, self).__init__(*args, **kwargs)
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

# Subject Management Forms
class CreateSubjectForm(FlaskForm):
    """Form for creating a new subject."""
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Create Subject')

    def validate_name(self, name):
        from app.services.subject_services import get_subject_by_name
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
            from app.services.subject_services import get_subject_by_name
            subject = get_subject_by_name(name.data)
            if subject:
                raise ValidationError('That subject name already exists. Please choose a different one.')

class DeleteSubjectForm(FlaskForm):
    """Form for deleting a subject."""
    confirm_delete = BooleanField('I confirm I want to delete this subject', validators=[DataRequired()])
    submit = SubmitField('Delete Subject')