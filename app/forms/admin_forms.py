from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User

class CreateUserForm(FlaskForm):
    """Form for creating a new user."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[("student","Student"),("teacher","Teacher"),("writer","Writer")], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    activated = BooleanField('Activated')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    submit = SubmitField('Create User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')
        
    def validate_role(self, role):
        if role.data not in ['admin', 'teacher', 'student', 'writer']:
            raise ValidationError('Invalid role. Must be one of: admin, teacher, student, writer.')
        

class UpdateUserForm(FlaskForm):
    """Form for updating an existing user."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    role = StringField('Role')
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[Length(min=2, max=20)])
    phone_number = StringField('Phone Number', validators=[Length(min=10, max=15)])
    profile_picture_filename = StringField('Profile Picture Filename')
    activated = BooleanField('Activated')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    submit = SubmitField('Update User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != self.username.data:
            raise ValidationError('That username is already taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != self.email.data:
            raise ValidationError('That email is already registered. Please choose a different one.')
        
    def validate_role(self, role):
        if role.data and role.data not in ['admin', 'teacher', 'student', 'writer']:
            raise ValidationError('Invalid role. Must be one of: admin, teacher, student, writer.')

class DeleteUserForm(FlaskForm):
    """Form for deleting a user."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Delete User')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('That username does not exist. Please choose a different one.')

