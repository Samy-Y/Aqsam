from flask import Blueprint, render_template, redirect, url_for, current_app
from app.forms.admin_forms import *
from app.services.user_services import get_user_by_id, create_user, delete_user, get_all_users, get_user_by_username, set_user_pfp
from app.services.class_services import create_class, delete_class, update_class, add_teacher_to_class, remove_teacher_from_class, get_all_classes, get_classes_by_teacher
from app.services.student_services import create_student, update_student, get_student_by_id, get_student_class_id_by_id
from app.services.teacher_services import create_teacher, update_teacher
from app.services.writer_services import create_writer, update_writer
from app.services.subject_services import update_subject, get_subject_by_id, create_subject, delete_subject, get_all_subjects
from app.routes.auth import current_user
from app.utils import format_date
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET', 'POST'])
def index():
    pfp_path = 'assets/profile_pictures/' + current_user.profile_picture_filename
    return render_template('admin/index.html',pfp_path=pfp_path)

# ===========================
# USER MANAGEMENT
# ===========================

# ---- USER VIEW ----
@admin_bp.route('/view_users', methods=['GET', 'POST'])
def view_users():
    pfp_form = ChangeUserProfilePictureForm()
    if pfp_form.validate_on_submit():
        user = get_user_by_id(int(pfp_form.user_id.data))
        new_profile_picture = pfp_form.profile_picture.data
        all_pfps = [user.profile_picture_filename for user in get_all_users()]
        if new_profile_picture:
            # delete the previous profile picture from static/assets/profile_pictures
            previous_pfp_path = os.path.join(current_app.instance_path.replace('/instance','/app'),'static/assets/profile_pictures', user.profile_picture_filename)
            if os.path.exists(previous_pfp_path):
                os.remove(previous_pfp_path)
            new_pfp_filename = secure_filename(new_pfp_filename)
            # manage filename conflicts
            if new_pfp_filename in all_pfps:
                new_pfp_filename = str(user.id) + '_' + new_pfp_filename
            set_user_pfp(user.id, new_pfp_filename)
            # save the new profile picture
            new_profile_picture.save(os.path.join(current_app.instance_path.replace('/instance','/app'),'static/assets/profile_pictures', user.profile_picture_filename))
            return redirect(url_for('admin.view_users'))
    users = get_all_users()
    return render_template('admin/view_users.html', users=users, form=pfp_form)

# ---- USER CREATION ----
@admin_bp.route('/create_user', methods=['GET', 'POST'])
def create_user_view():
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        activated = form.activated.data
        birth_date = format_date(form.date_of_birth.data)

        if username and password and role and first_name and last_name and birth_date:
            create_user(
                username=username,
                password=password,
                role=role,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                activated=activated,
                birth_date=birth_date
            )
        
        return redirect(url_for('admin.index'))
    return render_template('admin/create_user.html', form=form)

# ---- USER DELETION ----
@admin_bp.route('/delete_user', methods=['GET', 'POST'])
def delete_user_view():
    form = DeleteUserForm()
    if form.validate_on_submit():
        username = form.username.data
        user = get_user_by_username(username)
        if user:
            delete_user(user.id)
            return redirect(url_for('admin.index'))
    users = get_all_users()
    return render_template('admin/delete_user.html', form=form, users=users)

# ===========================
# CLASS MANAGEMENT
# ===========================

# ---- CLASS VIEW ----
@admin_bp.route('/view_classes', methods=['GET', 'POST'])
def view_classes():
    classes = get_all_classes()
    return render_template('admin/view_classes.html', classes=classes)

# ---- CLASS CREATION ----
@admin_bp.route('/create_class', methods=['GET', 'POST'])
def create_class_view():
    form = CreateClassForm()
    if form.validate_on_submit():
        class_name = form.name.data
        class_level = form.level.data
        if class_name and class_level:
            create_class(class_name, class_level)
            return redirect(url_for('admin.view_classes'))
    else:
        return render_template('admin/create_class.html', form=form, errors=form.errors)
    return render_template('admin/create_class.html', form=form)

# ---- CLASS UPDATE ----
@admin_bp.route('/update_class/<int:id>', methods=['GET', 'POST'])
def update_class_view(id):
    form = UpdateClassForm()
    class_obj = get_class_by_id(id)
    if form.validate_on_submit():
        class_id = id
        class_name = form.name.data
        class_level = form.level.data
        if class_id and class_name and class_level:
            update_class(class_id, class_name, class_level)
            return redirect(url_for('admin.view_classes'))
    else:
        form.name.data = class_obj.name
        form.level.data = class_obj.level
        return render_template('admin/update_class.html', form=form, errors=form.errors)
    return render_template('admin/update_class.html', form=form, classes=class_obj)

# ---- CLASS DELETION ----
@admin_bp.route('/delete_class/<int:id>', methods=['GET', 'POST'])
def delete_class_view(id):
    form = DeleteClassForm()
    if form.validate_on_submit():
        class_id = id
        if class_id:
            delete_class(class_id)
            return redirect(url_for('admin.view_classes'))
    classes = get_all_classes()
    return render_template('admin/delete_class.html', form=form, classes=classes)

# ===========================
# STUDENT MANAGEMENT
# ===========================

# ---- STUDENT VIEW ----
@admin_bp.route('/view_students', methods=['GET', 'POST'])
def view_students():
    students = get_all_users()
    return render_template('admin/view_students.html', students=students)

# ---- STUDENT CREATION ----
@admin_bp.route('/create_student', methods=['GET', 'POST'])
def create_student_view():
    form = CreateStudentForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        birth_date = form.birth_date.data
        phone_number = form.phone_number.data
        class_id = form.class_id.data
        if username and password and email and first_name and last_name and birth_date and class_id:
            create_student(username, 
                           password, 
                           email, 
                           first_name, 
                           last_name, 
                           birth_date, 
                           phone_number=phone_number, 
                           class_id=class_id)
            return redirect(url_for('admin.index'))
    return render_template('admin/create_student.html', form=form)

# ---- STUDENT UPDATE ----
@admin_bp.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student_view(id):
    form = UpdateStudentForm()
    student_usr = get_user_by_id(id)
    if form.validate_on_submit():
        student_id = id
        username = form.username.data
        new_password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        birth_date = form.birth_date.data
        phone_number = form.phone_number.data
        class_id = form.class_id.data
        if student_id and username and email and first_name and last_name and birth_date and class_id:
            update_student(student_id, username, email=email, first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number, class_id=class_id)
        if student_id and username and new_password:
            update_student(student_id, username=username, password=new_password)
        return redirect(url_for('admin.index'))
    else:
        form.username.data = student_usr.username
        form.email.data = student_usr.email
        form.first_name.data = student_usr.first_name
        form.last_name.data = student_usr.last_name
        form.birth_date.data = student_usr.birth_date
        form.phone_number.data = student_usr.phone_number
        form.class_id.data = get_student_class_id_by_id(id)
        print(form.errors)
        return render_template('admin/update_student.html', form=form,student_usr=student_usr, student_obj=get_student_by_id(id), errors=form.errors)
    return render_template('admin/update_student.html', form=form, student_usr=student_usr, student_obj=get_student_by_id(id))

# ===========================
# SUBJECT MANAGEMENT
# ===========================

# ---- SUBJECT VIEW ----
@admin_bp.route('/view_subjects', methods=['GET', 'POST'])
def view_subjects():
    subjects = get_all_subjects()
    return render_template('admin/view_subjects.html', subjects=subjects)

# ---- SUBJECT CREATION ----
@admin_bp.route('/create_subject', methods=['GET', 'POST'])
def create_subject_view():
    form = CreateSubjectForm()
    if form.validate_on_submit():
        subject_name = form.name.data
        if subject_name:
            create_subject(subject_name)
            return redirect(url_for('admin.view_subjects'))
    return render_template('admin/create_subject.html', form=form)

# ---- SUBJECT UPDATE ----
@admin_bp.route('/update_subject/<int:id>', methods=['GET', 'POST'])
def update_subject_view(id):
    form = UpdateSubjectForm()
    subject_obj = get_subject_by_id(id)
    if subject_obj is None:
        return redirect(url_for('admin.view_subjects'))  # Redirect or handle invalid ID
    if form.validate_on_submit():
        subject_id = id
        subject_name = form.name.data
        if subject_id and subject_name:
            update_subject(subject_id, subject_name)
            return redirect(url_for('admin.view_subjects'))
    else:
        form.name.data = subject_obj.name
        return render_template('admin/update_subject.html', form=form, errors=form.errors)
    return render_template('admin/update_subject.html', form=form, subjects=subject_obj)

# ---- SUBJECT DELETE ----
@admin_bp.route('/delete_subject/<int:id>', methods=['GET', 'POST'])
def delete_subject_view(id):
    form = DeleteSubjectForm()
    if form.validate_on_submit():
        subject_id = id
        if subject_id:
            delete_subject(subject_id)
            return redirect(url_for('admin.view_subjects'))
    subjects = get_all_subjects()
    return render_template('admin/delete_subject.html', form=form, subjects=subjects)

# ===========================
# TEACHER MANAGEMENT
# ===========================

# ---- TEACHER VIEW ----
@admin_bp.route('/view_teachers', methods=['GET', 'POST'])
def view_teachers():
    teachers = get_all_users()
    return render_template('admin/view_teachers.html', teachers=teachers)

# ---- TEACHER CREATION ----
@admin_bp.route('/create_teacher', methods=['GET', 'POST'])
def create_teacher_view():
    form = CreateTeacherForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        birth_date = format_date(form.date_of_birth.data)
        classes_id = form.classes_id.data
        subjects_id = form.subjects_id.data
        if username and password and email and first_name and last_name and birth_date and classes_id and subjects_id:
            create_teacher(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                classes_id=classes_id,
                subjects_id=subjects_id,
            )
            return redirect(url_for('admin.index'))
    return render_template('admin/create_teacher.html', form=form)

# ---- TEACHER UPDATE ----
@admin_bp.route('/update_teacher/<int:id>', methods=['GET', 'POST'])
def update_teacher_view(id):
    form = UpdateTeacherForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        birth_date = format_date(form.date_of_birth.data)
        classes_id = form.classes_id.data
        if username:
            update_teacher(id, username=username)
        if email:
            update_teacher(id, email=email)
        if first_name:
            update_teacher(id, first_name=first_name)
        if last_name:
            update_teacher(id, last_name=last_name)
        if birth_date:
            update_teacher(id, birth_date=birth_date)
        if classes_id:
            update_teacher(id, classes_id=classes_id)
        if password:
            update_teacher(id, password=password)
        if phone_number:
            update_teacher(id, phone_number=phone_number)
        return redirect(url_for('admin.index'))
    teachers = get_all_users()
    return render_template('admin/update_teacher.html', form=form, teachers=teachers)

# ===========================
# WRITER MANAGEMENT
# ===========================