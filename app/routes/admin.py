from flask import Blueprint, render_template, redirect, url_for
from app.forms.admin_forms import CreateUserForm, DeleteUserForm, CreateClassForm, DeleteClassForm, AssignTeacherForm
from app.services.user_services import create_user, delete_user, get_all_users
from app.services.class_services import create_class, delete_class, add_teacher_to_class, remove_teacher_from_class, get_all_classes, get_classes_by_teacher
from app.services.student_services import update_student
from app.services.teacher_services import update_teacher
from app.services.writer_services import update_writer
from app.routes.auth import current_user
from app.utils import format_date

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET', 'POST'])
def index():
    pfp_path = 'assets/profile_pictures/' + current_user.profile_picture_filename
    return render_template('admin/index.html',pfp_path=pfp_path)

@admin_bp.route('/user_management', methods=['GET', 'POST'])
def user_management():
    create_user_form = CreateUserForm()
    if create_user_form.validate_on_submit():
        username = create_user_form.username.data
        password = create_user_form.password.data
        role = create_user_form.role.data
        email = create_user_form.email.data
        first_name = create_user_form.first_name.data
        last_name = create_user_form.last_name.data
        phone_number = create_user_form.phone_number.data
        date_of_birth = format_date(create_user_form.date_of_birth.data)

        create_user(
            username=username,
            password=password,
            role=role,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            birth_date=date_of_birth
        )

        return redirect(url_for('admin.user_management',success=True))
    else:
        if create_user_form.errors:
            for field, errors in create_user_form.errors.items():
                return redirect(url_for('admin.user_management',failed=True,errors=errors))
            
    users = get_all_users()
    return render_template('admin/user_management.html',
                           create_user_form=create_user_form,
                           users=users)

@admin_bp.route('/class_management', methods=['GET', 'POST'])
def class_management():
    create_class_form = CreateClassForm()
    if create_class_form.validate_on_submit():
        name = create_class_form.name.data
        level = create_class_form.level.data

        create_class(
            name=name,
            level=level
        )

        return redirect(url_for('admin.class_management', success=True))
    else:
        if create_class_form.errors:
            for field, errors in create_class_form.errors.items():
                return redirect(url_for('admin.class_management', errors=errors))
            
    delete_class_form = DeleteClassForm()

    if delete_class_form.validate_on_submit():
        class_id = delete_class_form.class_id.data
        confirm_delete = delete_class_form.confirm_delete.data

        if confirm_delete:
            delete_class(class_id=class_id)
            return redirect(url_for('admin.class_management', success=True))
        else:
            return redirect(url_for('admin.class_management', error="Please confirm deletion."))

    classes = get_all_classes()

    return render_template('admin/class_management.html',
                           create_class_form=create_class_form,
                           delete_class_form=delete_class_form,
                           classes=classes)

@admin_bp.route('/teacher_management', methods=['GET', 'POST'])
def teacher_management():
    assign_teacher_form = AssignTeacherForm()
    if assign_teacher_form.validate_on_submit():
        class_id = assign_teacher_form.class_id.data
        teacher_id = assign_teacher_form.teacher_id.data
        add_teacher_to_class(
            class_id=class_id,
            teacher_id=teacher_id
        )
        return redirect(url_for('admin.teacher_management', success=True))
    else:
        if assign_teacher_form.errors:
            for field, errors in assign_teacher_form.errors.items():
                return redirect(url_for('admin.teacher_management', errors=errors))

    teachers = get_all_users(role='teacher')

    return render_template('admin/teacher_management.html',
                           assign_teacher_form=assign_teacher_form,
                           teacher=teachers)

@admin_bp.route('/student_management', methods=['GET', 'POST'])
def student_management():
    students = get_all_users(role='student')
    return render_template('admin/student_management.html', students=students)