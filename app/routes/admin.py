from flask import Blueprint, render_template, redirect, url_for, current_app
from app.forms.admin_forms import *
from app.services.user_services import get_user_by_id, create_user, delete_user, get_all_users, get_user_by_username, set_user_pfp
from app.services.class_services import create_class, delete_class, update_class, add_teacher_to_class, remove_teacher_from_class, get_all_classes, get_classes_by_teacher
from app.services.student_services import create_student, update_student, get_student_by_id, get_student_class_id_by_id
from app.services.teacher_services import create_teacher, update_teacher
from app.services.writer_services import create_writer, update_writer
from app.services.article_services import create_article, get_all_articles, get_article_by_id, update_article, delete_article
from app.services.subject_services import update_subject, get_subject_by_id, create_subject, delete_subject, get_all_subjects
from app.routes.auth import current_user
from app.utils import format_date
from werkzeug.utils import secure_filename
import os, json
from flask_login import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    pfp_path = 'assets/profile_pictures/' + current_user.profile_picture_filename
    return render_template('admin/index.html',pfp_path=pfp_path)

# ===========================
# USER MANAGEMENT
# ===========================

# ---- USER VIEW ----
@admin_bp.route('/view_users', methods=['GET', 'POST'])
@login_required
def view_users():
    pfp_form = ChangeUserProfilePictureForm()
    if pfp_form.validate_on_submit():
        user = get_user_by_id(int(pfp_form.user_id.data))
        new_profile_picture_file = pfp_form.profile_picture.data  # FileStorage object

        if new_profile_picture_file and new_profile_picture_file.filename:
            # 1. Delete the previous profile picture, if it exists and is not None
            if user.profile_picture_filename:
                previous_pfp_path = os.path.join(
                    current_app.instance_path.replace('/instance', '/app'),
                    'static/assets/profile_pictures',
                    user.profile_picture_filename
                )
                if os.path.exists(previous_pfp_path):
                    os.remove(previous_pfp_path)

            # 2. Prepare the new filename
            base_new_filename = secure_filename(new_profile_picture_file.filename)

            # 3. Manage filename conflicts
            # Get a list of all *existing* profile picture filenames, excluding None
            all_existing_filenames = [u.profile_picture_filename for u in get_all_users() if u.profile_picture_filename is not None]

            final_new_pfp_filename = base_new_filename
            # Check for conflict and prepend user_id if necessary
            # Ensure the check is against other users' pfps or if the new base name (after secure_filename) is the same as an existing one.
            # A simple conflict check:
            temp_filename_to_check = final_new_pfp_filename
            count = 0
            while temp_filename_to_check in all_existing_filenames:
                count += 1
                name, ext = os.path.splitext(base_new_filename)
                temp_filename_to_check = f"{name}_{str(user.id)}_{count}{ext}"  # More robust conflict resolution
            final_new_pfp_filename = temp_filename_to_check

            # If still in conflict after trying with user_id (e.g. user uploads same file again for themselves after it was made unique)
            # or if the initial name was already unique, this logic might need refinement based on exact requirements.
            # For now, let's use a simpler user_id prefix if the base_new_filename is in all_existing_filenames
            if base_new_filename in all_existing_filenames:
                # Check if the conflict is with another user or a different file from the same user
                is_self_conflict = any(u.id == user.id and u.profile_picture_filename == base_new_filename for u in get_all_users())
                if not is_self_conflict or base_new_filename != user.profile_picture_filename:  # if conflict is not with current user's current pfp
                    final_new_pfp_filename = str(user.id) + '_' + base_new_filename
                    # Re-check if this new unique name is also in conflict (highly unlikely but good practice)
                    if final_new_pfp_filename in all_existing_filenames:
                        name, ext = os.path.splitext(base_new_filename)
                        final_new_pfp_filename = f"{name}_{str(user.id)}_{os.urandom(4).hex()}{ext}"

            # 4. Update the user's profile picture filename in the database
            set_user_pfp(user.id, final_new_pfp_filename)

            # 5. Save the new profile picture file
            save_path = os.path.join(
                current_app.instance_path.replace('/instance', '/app'),
                'static/assets/profile_pictures',
                final_new_pfp_filename  # Use the finalized new filename
            )
            new_profile_picture_file.save(save_path)

            return redirect(url_for('admin.view_users'))
    users = get_all_users()
    return render_template('admin/view_users.html', users=users, form=pfp_form)

# ---- USER CREATION ----
@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
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
                email=email if email != '' else None,  # unique constraint check
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                activated=activated,
                birth_date=birth_date
            )
        
        return redirect(url_for('admin.view_users'))
    return render_template('admin/create_user.html', form=form)

# ---- USER DELETION ----
@admin_bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user_view():
    form = DeleteUserForm()
    if form.validate_on_submit():
        username = form.username.data
        user = get_user_by_username(username)
        if user:
            delete_user(user.id)
            return redirect(url_for('admin.view_users'))
    users = get_all_users()
    return render_template('admin/delete_user.html', form=form, users=users)

# ===========================
# CLASS MANAGEMENT
# ===========================

# ---- CLASS VIEW ----
@admin_bp.route('/view_classes', methods=['GET', 'POST'])
@login_required
def view_classes():
    classes = get_all_classes()
    return render_template('admin/view_classes.html', classes=classes)

# ---- CLASS CREATION ----
@admin_bp.route('/create_class', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
def view_students():
    pfp_form = ChangeUserProfilePictureForm()  # Instantiate the PFP form

    if pfp_form.validate_on_submit() and pfp_form.profile_picture.data:
        user_id_to_update = int(pfp_form.user_id.data)
        user = get_user_by_id(user_id_to_update)
        
        if user and user.role == 'student': # Ensure we're updating a student
            new_profile_picture_file = pfp_form.profile_picture.data
            if new_profile_picture_file and new_profile_picture_file.filename:
                # 1. Delete the previous profile picture, if it exists and is not None
                if user.profile_picture_filename:
                    previous_pfp_path = os.path.join(
                        current_app.instance_path.replace('/instance', '/app'),
                        'static/assets/profile_pictures',
                        user.profile_picture_filename
                    )
                    if os.path.exists(previous_pfp_path):
                        os.remove(previous_pfp_path)

                # 2. Prepare the new filename
                base_new_filename = secure_filename(new_profile_picture_file.filename)

                # 3. Manage filename conflicts
                all_existing_filenames = [u.profile_picture_filename for u in get_all_users() if u.profile_picture_filename is not None]
                final_new_pfp_filename = base_new_filename
                temp_filename_to_check = final_new_pfp_filename
                count = 0
                # Ensure the new filename is unique or belongs to the current user and is the same file
                while temp_filename_to_check in all_existing_filenames and not (user.profile_picture_filename == temp_filename_to_check and user.id == user_id_to_update):
                    count += 1
                    name, ext = os.path.splitext(base_new_filename)
                    temp_filename_to_check = f"{name}_{str(user.id)}_{count}{ext}"
                final_new_pfp_filename = temp_filename_to_check

                if base_new_filename in all_existing_filenames and not (user.profile_picture_filename == base_new_filename and user.id == user_id_to_update):
                    # Further conflict resolution if the generated name is still not unique
                    # This part of the logic might need refinement based on exact conflict rules desired
                    is_self_conflict_after_count = any(u.id == user.id and u.profile_picture_filename == final_new_pfp_filename for u in get_all_users())

                    if final_new_pfp_filename in all_existing_filenames and not is_self_conflict_after_count :
                         final_new_pfp_filename = str(user.id) + '_' + base_new_filename
                         if final_new_pfp_filename in all_existing_filenames and not (user.profile_picture_filename == final_new_pfp_filename and user.id == user_id_to_update):
                            name, ext = os.path.splitext(base_new_filename)
                            final_new_pfp_filename = f"{name}_{str(user.id)}_{os.urandom(4).hex()}{ext}"
                
                # 4. Update the user's profile picture filename in the database
                set_user_pfp(user.id, final_new_pfp_filename)

                # 5. Save the new profile picture file
                save_path = os.path.join(
                    current_app.instance_path.replace('/instance', '/app'),
                    'static/assets/profile_pictures',
                    final_new_pfp_filename
                )
                new_profile_picture_file.save(save_path)
                return redirect(url_for('admin.view_students'))

    students = get_all_users(role='student')
    student_classes = dict()
    for student_user_obj in students: # Changed variable name to avoid conflict
        class_id = get_student_class_id_by_id(student_user_obj.id)
        if class_id: # Check if class_id is not None
            class_obj = get_class_by_id(class_id)
            if class_obj: # Check if class_obj is not None
                student_classes[student_user_obj.id] = f'{class_obj.level} - {class_obj.name}'
            else:
                student_classes[student_user_obj.id] = 'Class not found' # Handle case where class_id is invalid
        else:
            student_classes[student_user_obj.id] = 'No class assigned' # Handle case where student has no class
            
    return render_template('admin/view_students.html', students=students, student_classes=student_classes, form=pfp_form) # Pass pfp_form

# ---- STUDENT CREATION ----
@admin_bp.route('/create_student', methods=['GET', 'POST'])
@login_required
def create_student_view():
    form = CreateStudentForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        birth_date = format_date(form.birth_date.data)
        phone_number = form.phone_number.data
        class_id = form.class_id.data
        create_student(username=username, 
                        password=password, 
                        email=email if email != '' else None, # unique constraint check
                        first_name=first_name, 
                        last_name=last_name, 
                        birth_date=birth_date, 
                        phone_number=phone_number, 
                        class_id=class_id)
        return redirect(url_for('admin.view_students'))
    return render_template('admin/create_student.html', form=form)

# ---- STUDENT UPDATE ----
@admin_bp.route('/update_student/<int:id>', methods=['GET', 'POST'])
@login_required
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
        birth_date = format_date(form.birth_date.data)
        phone_number = form.phone_number.data
        class_id = form.class_id.data
        if student_id and username:
            if new_password:
                update_student(student_id, password=new_password)
            if email and email != student_usr.email:
                update_student(student_id, email=email)
            if first_name and first_name != student_usr.first_name:
                update_student(student_id, first_name=first_name)
            if last_name and last_name != student_usr.last_name:
                update_student(student_id, last_name=last_name)
            if birth_date and birth_date != student_usr.birth_date:
                update_student(student_id, birth_date=birth_date)
            if phone_number and phone_number != student_usr.phone_number:
                update_student(student_id, phone_number=phone_number)
            if class_id and class_id != get_student_class_id_by_id(id):
                update_student(student_id, class_id=class_id)
        return redirect(url_for('admin.view_students'))
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
@login_required
def view_subjects():
    subjects = get_all_subjects()
    return render_template('admin/view_subjects.html', subjects=subjects)

# ---- SUBJECT CREATION ----
@admin_bp.route('/create_subject', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
def view_teachers():
    pfp_form = ChangeUserProfilePictureForm() # Instantiate the form
    if pfp_form.validate_on_submit():
        user = get_user_by_id(int(pfp_form.user_id.data))
        new_profile_picture_file = pfp_form.profile_picture.data

        if new_profile_picture_file and new_profile_picture_file.filename:
            if user.profile_picture_filename:
                previous_pfp_path = os.path.join(
                    current_app.instance_path.replace('/instance', '/app'),
                    'static/assets/profile_pictures',
                    user.profile_picture_filename
                )
                if os.path.exists(previous_pfp_path):
                    os.remove(previous_pfp_path)

            base_new_filename = secure_filename(new_profile_picture_file.filename)
            all_existing_filenames = [u.profile_picture_filename for u in get_all_users() if u.profile_picture_filename is not None]
            final_new_pfp_filename = base_new_filename
            temp_filename_to_check = final_new_pfp_filename
            count = 0
            while temp_filename_to_check in all_existing_filenames:
                count += 1
                name, ext = os.path.splitext(base_new_filename)
                temp_filename_to_check = f"{name}_{str(user.id)}_{count}{ext}"
            final_new_pfp_filename = temp_filename_to_check

            if base_new_filename in all_existing_filenames:
                is_self_conflict = any(u.id == user.id and u.profile_picture_filename == base_new_filename for u in get_all_users())
                if not is_self_conflict or base_new_filename != user.profile_picture_filename:
                    final_new_pfp_filename = str(user.id) + '_' + base_new_filename
                    if final_new_pfp_filename in all_existing_filenames:
                        name, ext = os.path.splitext(base_new_filename)
                        final_new_pfp_filename = f"{name}_{str(user.id)}_{os.urandom(4).hex()}{ext}"
            
            set_user_pfp(user.id, final_new_pfp_filename)
            save_path = os.path.join(
                current_app.instance_path.replace('/instance', '/app'),
                'static/assets/profile_pictures',
                final_new_pfp_filename
            )
            new_profile_picture_file.save(save_path)
            return redirect(url_for('admin.view_teachers')) # Redirect back to view_teachers

    teachers = get_all_users(role='teacher')
    teacher_classes_data = dict()
    for teacher in teachers:
        teacher_classes_list = get_classes_by_teacher(teacher.id)
        teacher_classes_data[teacher.id] = [f'{class_obj.level} - {class_obj.name}' for class_obj in teacher_classes_list]
    return render_template('admin/view_teachers.html', teachers=teachers, teacher_classes=teacher_classes_data, form=pfp_form) # Pass the form

# ---- TEACHER CREATION ----
@admin_bp.route('/create_teacher', methods=['GET', 'POST'])
@login_required
def create_teacher_view():
    form = CreateTeacherForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        birth_date = format_date(form.date_of_birth.data)
        phone_number = form.phone_number.data
        classes_id = form.classes_id.data
        print(classes_id)
        subjects_id = form.subjects_id.data
        create_teacher(
            username=username,
            password=password,
            email=email if email != '' else None,  # unique constraint check
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            phone_number=phone_number,
            classes_ids=classes_id,
            subjects_ids=subjects_id
        )
        return redirect(url_for('admin.view_teachers'))
    return render_template('admin/create_teacher.html', form=form)

# ---- TEACHER UPDATE ----
@admin_bp.route('/update_teacher/<int:id>', methods=['GET', 'POST'])
@login_required
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
        subjects_id = form.subjects_id.data
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
        if subjects_id:
            update_teacher(id, subjects_id=subjects_id)
        return redirect(url_for('admin.view_teachers'))
    teachers = get_all_users()
    return render_template('admin/update_teacher.html', form=form, teachers=teachers)

# ===========================
# WRITER MANAGEMENT
# ===========================

# ---- WRITER VIEW ----
@admin_bp.route('/view_writers', methods=['GET', 'POST'])
@login_required
def view_writers():
    pfp_form = ChangeUserProfilePictureForm()
    if pfp_form.validate_on_submit() and pfp_form.profile_picture.data:
        user_id_to_update = int(pfp_form.user_id.data)
        user = get_user_by_id(user_id_to_update)
        
        if user and user.role == 'writer': # Ensure we're updating a writer
            new_profile_picture_file = pfp_form.profile_picture.data
            if new_profile_picture_file and new_profile_picture_file.filename:
                if user.profile_picture_filename:
                    previous_pfp_path = os.path.join(current_app.instance_path.replace('/instance', '/app'), 'static/assets/profile_pictures', user.profile_picture_filename)
                    if os.path.exists(previous_pfp_path):
                        os.remove(previous_pfp_path)

                base_new_filename = secure_filename(new_profile_picture_file.filename)
                all_existing_filenames = [u.profile_picture_filename for u in get_all_users() if u.profile_picture_filename is not None]
                final_new_pfp_filename = base_new_filename
                temp_filename_to_check = final_new_pfp_filename
                count = 0
                while temp_filename_to_check in all_existing_filenames and not (user.profile_picture_filename == temp_filename_to_check and user.id == user_id_to_update):
                    count += 1
                    name, ext = os.path.splitext(base_new_filename)
                    temp_filename_to_check = f"{name}_{str(user.id)}_{count}{ext}"
                final_new_pfp_filename = temp_filename_to_check

                if base_new_filename in all_existing_filenames and not (user.profile_picture_filename == base_new_filename and user.id == user_id_to_update):
                    is_self_conflict_after_count = any(u.id == user.id and u.profile_picture_filename == final_new_pfp_filename for u in get_all_users())
                    if final_new_pfp_filename in all_existing_filenames and not is_self_conflict_after_count :
                         final_new_pfp_filename = str(user.id) + '_' + base_new_filename
                         if final_new_pfp_filename in all_existing_filenames and not (user.profile_picture_filename == final_new_pfp_filename and user.id == user_id_to_update):
                            name, ext = os.path.splitext(base_new_filename)
                            final_new_pfp_filename = f"{name}_{str(user.id)}_{os.urandom(4).hex()}{ext}"
                
                set_user_pfp(user.id, final_new_pfp_filename)
                save_path = os.path.join(current_app.instance_path.replace('/instance', '/app'), 'static/assets/profile_pictures', final_new_pfp_filename)
                new_profile_picture_file.save(save_path)
                return redirect(url_for('admin.view_writers'))

    writers = get_all_users(role='writer') # Fetches user objects with role 'writer'
    return render_template('admin/view_writers.html', writers=writers, form=pfp_form)

# ---- WRITER CREATION ----
@admin_bp.route('/create_writer', methods=['GET', 'POST'])
@login_required
def create_writer_view():
    form = CreateWriterForm()
    if form.validate_on_submit():
        create_writer( # This service creates both User and Writer records
            username=form.username.data,
            password=form.password.data,
            email=form.email.data if form.email.data else None,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            birth_date=format_date(form.date_of_birth.data) if form.date_of_birth.data else None,
            phone_number=form.phone_number.data if form.phone_number.data else None
            # 'activated' is handled by user_services.create_user default or can be added to form
        )
        # flash('Writer created successfully!', 'success') # Optional
        return redirect(url_for('admin.view_writers'))
    return render_template('admin/create_writer.html', form=form)

# ---- WRITER UPDATE ----
@admin_bp.route('/update_writer/<int:id>', methods=['GET', 'POST'])
@login_required
def update_writer_view(id):
    writer_user = get_user_by_id(id)
    if not writer_user or writer_user.role != 'writer':
        # flash('Writer not found.', 'error') # Optional
        return redirect(url_for('admin.view_writers'))

    form = UpdateWriterForm(original_username=writer_user.username, original_email=writer_user.email)
    
    if form.validate_on_submit():
        update_writer( # This service updates the User part of the Writer
            writer_id=id, # writer_id is the same as user_id for writers
            username=form.username.data,
            password=form.password.data if form.password.data else None,
            email=form.email.data if form.email.data else None,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            birth_date=format_date(form.date_of_birth.data) if form.date_of_birth.data else None,
            phone_number=form.phone_number.data if form.phone_number.data else None
        )
        # Update activation status if needed (user_services)
        if writer_user.activated != form.activated.data:
            # Assuming a service like update_user_activation(user_id, activated_status)
            # For now, let's assume user_services.update_user handles this or you add it
            writer_user.activated = form.activated.data 
            db.session.commit()


        # flash('Writer updated successfully!', 'success') # Optional
        return redirect(url_for('admin.view_writers'))
    
    # Populate form with existing data for GET request
    form.username.data = writer_user.username
    form.email.data = writer_user.email
    form.first_name.data = writer_user.first_name
    form.last_name.data = writer_user.last_name
    form.phone_number.data = writer_user.phone_number
    form.date_of_birth.data = writer_user.birth_date # This is already a date object
    form.activated.data = writer_user.activated
    
    return render_template('admin/update_writer.html', form=form, writer_id=id)


# ===========================
# ARTICLE MANAGEMENT
# ===========================

# ---- ARTICLE VIEW ----
@admin_bp.route('/view_articles', methods=['GET'])
@login_required
def view_articles():
    articles = get_all_articles()
    return render_template('admin/view_articles.html', articles=articles)

# ---- ARTICLE CREATION ----
@admin_bp.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article_view():
    form = CreateArticleForm()
    if form.validate_on_submit():
        if form.author_id.data == 0 : # Check for placeholder "No writers available"
             # flash("Cannot create article without a valid author.", "error") # Optional
             return render_template('admin/create_article.html', form=form)

        create_article(
            title=form.title.data,
            content_md=form.content_md.data,
            author_id=form.author_id.data,
            is_published=form.is_published.data
        )
        # flash('Article created successfully!', 'success') # Optional
        return redirect(url_for('admin.view_articles'))
    return render_template('admin/create_article.html', form=form)

# ---- ARTICLE UPDATE ----
@admin_bp.route('/update_article/<int:id>', methods=['GET', 'POST'])
@login_required
def update_article_view(id):
    article = get_article_by_id(id)
    if not article:
        # flash('Article not found.', 'error') # Optional
        return redirect(url_for('admin.view_articles'))
    
    form = UpdateArticleForm(obj=article) # Pre-populate form with article data

    if form.validate_on_submit():
        if form.author_id.data == 0 : # Check for placeholder "No writers available"
             # flash("Cannot update article without a valid author.", "error") # Optional
             # Repopulate form for rendering
             form.title.data = article.title
             form.content_md.data = article.content_md
             form.is_published.data = article.is_published
             # Keep selected author if it was valid, or reset if it became invalid
             # This part might need more robust handling if authors can be deleted
             # For now, we assume the list is up-to-date.
             return render_template('admin/update_article.html', form=form, article_id=id)

        update_article(
            article_id=id,
            title=form.title.data,
            content_md=form.content_md.data,
            author_id=form.author_id.data,
            is_published=form.is_published.data
        )
        # flash('Article updated successfully!', 'success') # Optional
        return redirect(url_for('admin.view_articles'))
    
    # For GET request, obj=article in form constructor already populates fields.
    # If you need to set choices dynamically or handle specific cases for GET:
    # form.title.data = article.title
    # form.content_md.data = article.content_md
    # form.author_id.data = article.author_id
    # form.is_published.data = article.is_published
    
    return render_template('admin/update_article.html', form=form, article_id=id)

# ---- ARTICLE DELETE ----
@admin_bp.route('/delete_article/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_article_view(id):
    article = get_article_by_id(id)
    if not article:
        # flash('Article not found.', 'error') # Optional
        return redirect(url_for('admin.view_articles'))
        
    form = DeleteArticleForm()
    if form.validate_on_submit():
        if form.confirm_delete.data:
            delete_article(id)
            # flash('Article deleted successfully.', 'success') # Optional
            return redirect(url_for('admin.view_articles'))
    return render_template('admin/delete_article.html', form=form, article=article)

# ===========================
# SCHOOL SETTINGS
# ===========================

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SchoolSettingsForm()
    
    school_info_path = os.path.join('..', current_app.instance_path, 'school_info.json')

    if form.validate_on_submit():
        school_name = form.school_name.data
        school_address = form.school_address.data
        school_phone = form.school_phone.data
        school_email = form.school_email.data
        school_website = form.school_website.data

        if os.path.exists(school_info_path):
            with open(school_info_path, 'r+', encoding='utf-8') as f:
                school_info = json.load(f)

        school_info['school_name'] = school_name
        school_info['school_address'] = school_address
        school_info['school_phone'] = school_phone
        school_info['school_email'] = school_email
        school_info['school_website'] = school_website
        
        with open(school_info_path, 'w', encoding='utf-8') as f:
            json.dump(school_info, f, indent=4)

        # Logo upload handling
        if form.school_logo.data:
            logo_file = form.school_logo.data
            logo_filename = secure_filename(logo_file.filename)
            
            relative_logo_save_dir = os.path.join('assets', 'uploads')
            logo_save_dir = os.path.join(current_app.static_folder, relative_logo_save_dir)
            os.makedirs(logo_save_dir, exist_ok=True)
            
            full_logo_save_path = os.path.join(logo_save_dir, logo_filename)
            logo_file.save(full_logo_save_path)
            
            school_info['school_logo_filename'] = logo_filename 
            
            with open(school_info_path, 'w', encoding='utf-8') as f:
                json.dump(school_info, f, indent=4)
        
        return redirect(url_for('admin.settings')) 
    else:
        school_info = {}
        if os.path.exists(school_info_path):
            with open(school_info_path, 'r', encoding='utf-8') as f:
                school_info = json.load(f)
        print(school_info)
        form.school_name.data = school_info.get('school_name', '')
        form.school_address.data = school_info.get('school_address', '')
        form.school_phone.data = school_info.get('school_phone', '')
        form.school_email.data = school_info.get('school_email', '')
        form.school_website.data = school_info.get('school_website', '')
        # The template will display the current logo based on school_info!

    return render_template('admin/settings.html', form=form, school_info=school_info)