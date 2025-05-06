from flask import Blueprint, render_template, redirect, url_for
from app.forms.admin_forms import CreateUserForm, UpdateUserForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET', 'POST'])
def index():
    create_user_form = CreateUserForm()
    if create_user_form.validate_on_submit():
        # Process the form data and create a new user
        username = create_user_form.username.data
        password = create_user_form.password.data
        role = create_user_form.role.data
        email = create_user_form.email.data
        first_name = create_user_form.first_name.data
        last_name = create_user_form.last_name.data
        phone_number = create_user_form.phone_number.data
        date_of_birth = create_user_form.date_of_birth.data

        # Call the service to create the user (assuming you have a function for this)
        # user = user_services.create_user(username, password, role, email, first_name, last_name, date_of_birth, phone_number)

        # Redirect or flash a message after successful creation
        # flash('User created successfully!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/index.html',create_user_form=create_user_form)