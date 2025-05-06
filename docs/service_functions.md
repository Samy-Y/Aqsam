# Service Functions

This document provides comprehensive documentation for all service functions in the Aqsam application, including concrete examples and important notes for developers. Use to the table of contents located on the left side for quick navigation.

## User Services

User services handle core user management functionality, including account creation, verification, and authentication.

### `get_user_by_id(user_id: int) -> Optional[User]`

Retrieves a user by their ID.

**Example:**
```python
user = get_user_by_id(1)
if user:
    print(f"Found user: {user.username}")
else:
    print("User not found")
```

### `get_student_by_id(student_id: int) -> Optional[Student]`

Retrieves a student by their ID.

**Example:**
```python
student = get_student_by_id(1)
if student:
    print(f"Found student: {student.user.username}")
else:
    print("Student not found")
```

### `get_teacher_by_id(teacher_id: int) -> Optional[Teacher]`

Retrieves a teacher by their ID.

**Example:**
```python
teacher = get_teacher_by_id(1)
if teacher:
    print(f"Found teacher: {teacher.user.username}")
else:
    print("Teacher not found")
```

### `get_writer_by_id(writer_id: int) -> Optional[Writer]`

Retrieves a writer by their ID.

**Example:**
```python
writer = get_writer_by_id(1)
if writer:
    print(f"Found writer: {writer.user.username}")
else:
    print("Writer not found")
```

### `get_user_by_email(email: str) -> Optional[User]`

Retrieves a user by their email address.

**Example:**
```python
user = get_user_by_email("john.doe@example.com")
if user:
    print(f"Found user: {user.username}")
else:
    print("User not found")
```

### `get_user_by_username(username: str) -> Optional[User]`

Retrieves a user by their username.

**Example:**
```python
user = get_user_by_username("johndoe")
if user:
    print(f"Found user: {user.id}")
else:
    print("User not found")
```

### `get_users_by_role(role: str) -> List[User]`

Retrieves all users with a specific role.

**Example:**
```python
teachers = get_users_by_role("teacher")
print(f"Found {len(teachers)} teachers")
```

### `delete_user(user: User) -> bool`

Soft deletes a user by setting their `activated` flag to `False`.

**⚠️ Warning:** This is a soft delete that deactivates the user but keeps their record in the database.

**Example:**
```python
user = get_user_by_id(1)
if delete_user(user):
    print("User deactivated successfully")
else:
    print("Failed to deactivate user")
```

### `generate_email_verification_token(user: User, expiry_hours: int = 24) -> str`

Generates a token for email verification.

**Example:**
```python
user = get_user_by_id(1)
token = generate_email_verification_token(user)
print(f"Verification token: {token}")
# Send this token in an email to the user
```

### `verify_email(token: str) -> Optional[User]`

Verifies a user's email using a verification token.

**Example:**
```python
user = verify_email("verification_token_from_email")
if user:
    print("Email verified successfully")
else:
    print("Invalid or expired verification token")
```

### `generate_password_reset_token(user: User, expiry_hours: int = 1) -> str`

Generates a token for password reset.

**Example:**
```python
user = get_user_by_email("user@example.com")
token = generate_password_reset_token(user)
print(f"Password reset token: {token}")
# Send this token to user's email
```

### `reset_password(token: str, new_password: str) -> Optional[User]`

Resets a user's password using a reset token.

**Example:**
```python
user = reset_password("reset_token_from_email", "new_secure_password")
if user:
    print("Password reset successfully")
else:
    print("Invalid or expired reset token")
```

### `activate_user(user: User) -> bool`

Activates a user account.

**Example:**
```python
user = get_user_by_id(1)
if activate_user(user):
    print("User activated successfully")
```

### `deactivate_user(user: User) -> bool`

Deactivates a user account.

**Example:**
```python
user = get_user_by_id(1)
if deactivate_user(user):
    print("User deactivated successfully")
```

### `is_account_active(user: User) -> bool`

Checks if a user account is active.

**Example:**
```python
user = get_user_by_id(1)
if is_account_active(user):
    print("User account is active")
else:
    print("User account is deactivated")
```

### `create_user(username: str, password: str, role: str, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, birth_date: Optional[str] = None, phone_number: Optional[str] = None) -> User`

Creates a new user.

**⚠️ Note:** The `birth_date` parameter should be provided as a string in 'YYYY-MM-DD' format, which will be converted to a date object internally.

**⚠️ Note:** The `profile_picture_filename` parameter present in the User Model can only be changed after the creation of the user. By default, the profile picture filename is set to `NULL` and replaced by a placeholder on the frontend.

**Example:**
```python
user = create_user(
    username="johndoe",
    password="secure_password",
    role="student",
    email="john.doe@example.com",
    first_name="John",
    last_name="Doe",
    birth_date="1995-05-15",
    phone_number="+1234567890"
)
print(f"Created new user with ID: {user.id}")
```

### `set_user_pfp(user_id: int, pfp_filename: str) -> bool`

Sets the user's profile picture to the indicated filename stored in assets/profile_pictures.

## Student Services

Student services manage student-specific operations.

### `create_student(username: str, password: str, email: str, first_name: str, last_name: str, birth_date: str, phone_number: str, class_id: Optional[int] = None) -> Student`

Creates a new student.

**Example:**
```python
student = create_student(
    username="student1",
    password="secure_password",
    email="student@example.com",
    first_name="Jane",
    last_name="Smith",
    birth_date="2005-10-15",  # Format: YYYY-MM-DD
    phone_number="+1234567890",
    class_id=3  # Optional class ID
)
print(f"Created student with ID: {student.id}")
```

### `update_student(student_id: int, username: Optional[str] = None, password: Optional[str] = None, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, birth_date: Optional[str] = None, phone_number: Optional[str] = None, class_id: Optional[int] = None) -> Student`

Updates a student's information.

**Example:**
```python
updated_student = update_student(
    student_id=1,
    email="new.email@example.com",
    phone_number="+9876543210",
    class_id=4
)
if updated_student:
    print("Student updated successfully")
else:
    print("Student not found")
```

### `get_all_student_by_class_id(class_id: int) -> List[Student]`

Retrieves all students in a specific class.

**Example:**
```python
students = get_all_student_by_class_id(3)
print(f"Found {len(students)} students in the class")
for student in students:
    print(f"- {student.user.first_name} {student.user.last_name}")
```

## Teacher Services

Teacher services manage teacher-specific operations.

### `create_teacher(username: str, password: str, email: str, first_name: str, last_name: str, birth_date: str, phone_number: str, subjects: List = None, classes: List = None) -> Teacher`

Creates a new teacher.

**Example:**
```python
# First, get subjects and classes if you want to associate them
math_subject = get_subject_by_name("Mathematics")
physics_subject = get_subject_by_name("Physics")
class_9a = get_class_by_name("9A")

teacher = create_teacher(
    username="mssmith",
    password="secure_password",
    email="teacher@example.com",
    first_name="Mary",
    last_name="Smith",
    birth_date="1980-05-12",  # Format: YYYY-MM-DD
    phone_number="+1234567890",
    subjects=[math_subject, physics_subject],  # Optional
    classes=[class_9a]  # Optional
)
print(f"Created teacher with ID: {teacher.id}")
```

### `update_teacher(teacher_id: int, **kwargs) -> Optional[Teacher]`

Updates a teacher's information using keyword arguments.

**Example:**
```python
updated_teacher = update_teacher(
    teacher_id=1,
    username="msmith_new",
    email="mary.smith@newschool.edu",
    phone_number="+9876543210"
)
if updated_teacher:
    print("Teacher updated successfully")
else:
    print("Teacher not found")
```

### `add_subject_to_teacher(teacher_id: int, subject) -> Optional[Teacher]`

Adds a subject to a teacher's list of subjects.

**Example:**
```python
chemistry = get_subject_by_name("Chemistry")
teacher = add_subject_to_teacher(1, chemistry)
if teacher:
    print(f"Added Chemistry to teacher's subjects. Now teaches {len(teacher.subjects)} subjects")
```

### `remove_subject_from_teacher(teacher_id: int, subject) -> Optional[Teacher]`

Removes a subject from a teacher's list of subjects.

**Example:**
```python
physics = get_subject_by_name("Physics")
teacher = remove_subject_from_teacher(1, physics)
if teacher:
    print(f"Removed Physics from teacher's subjects")
```

### `add_class_to_teacher(teacher_id: int, class_obj) -> Optional[Teacher]`

Adds a class to a teacher's list of classes.

**Example:**
```python
class_10b = get_class_by_name("10B")
teacher = add_class_to_teacher(1, class_10b)
if teacher:
    print(f"Added class 10B to teacher. Now teaches {len(teacher.classes)} classes")
```

### `remove_class_from_teacher(teacher_id: int, class_obj) -> Optional[Teacher]`

Removes a class from a teacher's list of classes.

**Example:**
```python
class_9a = get_class_by_name("9A")
teacher = remove_class_from_teacher(1, class_9a)
if teacher:
    print(f"Removed class 9A from teacher")
```

### `get_teachers_by_subject(subject) -> List[Teacher]`

Retrieves all teachers who teach a specific subject.

**Example:**
```python
math = get_subject_by_name("Mathematics")
teachers = get_teachers_by_subject(math)
print(f"Found {len(teachers)} teachers who teach Mathematics")
```

## Writer Services

Writer services manage writer-specific operations.

### `create_writer(username: Optional[str] = None, password: Optional[str] = None, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, birth_date: Optional[str] = None, phone_number: Optional[str] = None) -> Writer`

Creates a new writer.

**⚠️ Warning:** All parameters are marked as optional, but some may actually be required by the underlying `create_user` function.

**Example:**
```python
writer = create_writer(
    username="journalist1",
    password="secure_password",
    email="writer@magazine.com",
    first_name="James",
    last_name="Johnson",
    birth_date="1988-07-23",  # Format: YYYY-MM-DD
    phone_number="+1234567890"
)
print(f"Created writer with ID: {writer.id}")
```

### `update_writer(writer_id: int, username: Optional[str] = None, password: Optional[str] = None, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, birth_date: Optional[str] = None, phone_number: Optional[str] = None) -> Writer`

Updates a writer's information.

**Example:**
```python
updated_writer = update_writer(
    writer_id=1,
    username="jjohnson_senior",
    email="james.johnson@magazine.com",
    phone_number="+9876543210"
)
if updated_writer:
    print("Writer updated successfully")
else:
    print("Writer not found")
```

### `get_all_authored_articles(writer_id: int) -> List[Article]`

Retrieves all articles authored by a specific writer.

**Example:**
```python
articles = get_all_authored_articles(1)
print(f"Writer has authored {len(articles)} articles")
for article in articles:
    print(f"- {article.title} ({'Published' if article.is_published else 'Draft'})")
```

## Article Services

Article services manage operations related to articles.

### `create_article(title: str, content_md: str, author_id: int, is_published: Optional[bool] = False) -> Article`

Creates a new article.

**Example:**
```python
article = create_article(
    title="Understanding Machine Learning",
    content_md="# Introduction\nMachine learning is a fascinating field...",
    author_id=1,
    is_published=False  # Default is draft (not published)
)
print(f"Created article with ID: {article.id}")
```

### `update_article(article_id: int, title: Optional[str] = None, author_id: Optional[int] = None, content_md: Optional[str] = None, is_published: Optional[bool] = None) -> Article`

Updates an article's information.

**Example:**
```python
updated_article = update_article(
    article_id=1,
    title="Advanced Machine Learning Concepts",
    content_md="# Updated Introduction\nMachine learning has evolved...",
    is_published=True  # Publish the article
)
if updated_article:
    print(f"Article updated and published on {updated_article.last_edited}")
else:
    print("Article not found")
```

### `delete_article(article_id: int) -> bool`

Deletes an article.

**⚠️ Warning:** This is a hard delete that completely removes the article from the database.

**Example:**
```python
if delete_article(1):
    print("Article deleted successfully")
else:
    print("Article not found or could not be deleted")
```

## Class Services

Class services manage operations related to school classes.

### `create_class(name: str, level: str) -> Optional[Class]`

Creates a new class.

**Example:**
```python
class_obj = create_class(
    name="9A",
    level="Grade 9"
)
print(f"Created class with ID: {class_obj.id}")
```

### `update_class(class_id: int, name: Optional[str] = None, level: Optional[str] = None) -> Optional[Class]`

Updates a class's information.

**Example:**
```python
updated_class = update_class(
    class_id=1,
    name="9B",
    level="Grade 9 Advanced"
)
if updated_class:
    print("Class updated successfully")
else:
    print("Class not found")
```

### `delete_class(class_id: int) -> bool`

Deletes a class.

**⚠️ Warning:** This is a hard delete that completely removes the class from the database. Consider the impact on related students and teachers before deletion.

**Example:**
```python
if delete_class(1):
    print("Class deleted successfully")
else:
    print("Class not found or could not be deleted")
```

### `get_class_by_id(class_id: int) -> Optional[Class]`

Retrieves a class by its ID.

**Example:**
```python
class_obj = get_class_by_id(1)
if class_obj:
    print(f"Found class: {class_obj.name}, Level: {class_obj.level}")
else:
    print("Class not found")
```

### `get_class_by_name(name: str) -> Optional[Class]`

Retrieves a class by its name.

**Example:**
```python
class_obj = get_class_by_name("9A")
if class_obj:
    print(f"Found class ID: {class_obj.id}, Level: {class_obj.level}")
else:
    print("Class not found")
```

### `get_classes_by_level(level: str) -> List[Class]`

Retrieves all classes at a specific level.

**Example:**
```python
classes = get_classes_by_level("Grade 9")
print(f"Found {len(classes)} classes at Grade 9 level")
for class_obj in classes:
    print(f"- {class_obj.name}")
```

### `get_all_classes() -> List[Class]`

Retrieves all classes.

**Example:**
```python
classes = get_all_classes()
print(f"Total classes: {len(classes)}")
```

### `add_teacher_to_class(class_id: int, teacher_id: int) -> Optional[Class]`

Adds a teacher to a class.

**Example:**
```python
class_obj = add_teacher_to_class(1, 2)
if class_obj:
    print(f"Teacher assigned to class {class_obj.name}")
else:
    print("Class or teacher not found")
```

### `remove_teacher_from_class(class_id: int, teacher_id: int) -> Optional[Class]`

Removes a teacher from a class.

**Example:**
```python
class_obj = remove_teacher_from_class(1, 2)
if class_obj:
    print(f"Teacher removed from class {class_obj.name}")
else:
    print("Class or teacher not found, or teacher not assigned to class")
```

### `get_classes_by_teacher(teacher_id: int) -> List[Class]`

Retrieves all classes taught by a specific teacher.

**Example:**
```python
classes = get_classes_by_teacher(1)
print(f"Teacher teaches {len(classes)} classes")
for class_obj in classes:
    print(f"- {class_obj.name}")
```

### `get_student_count_in_class(class_id: int) -> int`

Gets the number of students in a class.

**Example:**
```python
count = get_student_count_in_class(1)
print(f"Class has {count} students enrolled")
```

## Subject Services

Subject services manage operations related to academic subjects.

### `create_subject(name: str) -> Optional[Subject]`

Creates a new subject.

**Example:**
```python
subject = create_subject("Physics")
if subject:
    print(f"Created subject with ID: {subject.id}")
else:
    print("Failed to create subject")
```

### `update_subject(subject_id: int, name: Optional[str] = None) -> Optional[Subject]`

Updates a subject's information.

**Example:**
```python
updated_subject = update_subject(
    subject_id=1,
    name="Advanced Physics"
)
if updated_subject:
    print("Subject updated successfully")
else:
    print("Subject not found")
```

### `delete_subject(subject_id: int) -> bool`

Deletes a subject.

**⚠️ Warning:** This is a hard delete that completely removes the subject from the database. Consider the impact on related grades and teachers before deletion.

**Example:**
```python
if delete_subject(1):
    print("Subject deleted successfully")
else:
    print("Subject not found or could not be deleted")
```

### `get_subject_by_id(subject_id: int) -> Optional[Subject]`

Retrieves a subject by its ID.

**Example:**
```python
subject = get_subject_by_id(1)
if subject:
    print(f"Found subject: {subject.name}")
else:
    print("Subject not found")
```

### `get_subject_by_name(name: str) -> Optional[Subject]`

Retrieves a subject by its name.

**Example:**
```python
subject = get_subject_by_name("Mathematics")
if subject:
    print(f"Found subject ID: {subject.id}")
else:
    print("Subject not found")
```

## Grade Services

Grade services manage operations related to student grades.

### `create_grade(student_id: int, subject_id: int, teacher_id: int, grade: float, comment: Optional[str] = None) -> Optional[Grade]`

Creates a new grade for a student.

**Example:**
```python
new_grade = create_grade(
    student_id=1,
    subject_id=2,
    teacher_id=3,
    grade=85.5,
    comment="Excellent work on the project"
)
if new_grade:
    print(f"Created grade entry with ID: {new_grade.id}")
else:
    print("Failed to create grade entry")
```

### `update_grade(grade_id: int, grade: Optional[float] = None, comment: Optional[str] = None) -> Optional[Grade]`

Updates a grade's information.

**Example:**
```python
updated_grade = update_grade(
    grade_id=1,
    grade=88.0,
    comment="After review, grade adjusted upward"
)
if updated_grade:
    print("Grade updated successfully")
else:
    print("Grade entry not found")
```

### `delete_grade(grade_id: int) -> bool`

Deletes a grade.

**Example:**
```python
if delete_grade(1):
    print("Grade deleted successfully")
else:
    print("Grade not found or could not be deleted")
```

### `get_grade_by_id(grade_id: int) -> Optional[Grade]`

Retrieves a grade by its ID.

**Example:**
```python
grade = get_grade_by_id(1)
if grade:
    print(f"Grade: {grade.grade}, Subject: {grade.subject.name}")
else:
    print("Grade not found")
```

### `get_grades_by_student(student_id: int) -> List[Grade]`

Retrieves all grades for a specific student.

**Example:**
```python
grades = get_grades_by_student(1)
print(f"Student has {len(grades)} grade entries")
for grade in grades:
    print(f"- {grade.subject.name}: {grade.grade}")
```

### `get_grades_by_subject(subject_id: int) -> List[Grade]`

Retrieves all grades for a specific subject.

**Example:**
```python
grades = get_grades_by_subject(1)
print(f"Subject has {len(grades)} grade entries")
```

### `get_grades_by_teacher(teacher_id: int) -> List[Grade]`

Retrieves all grades assigned by a specific teacher.

**Example:**
```python
grades = get_grades_by_teacher(1)
print(f"Teacher has assigned {len(grades)} grades")
```

### `get_grades_by_student_and_subject(student_id: int, subject_id: int) -> List[Grade]`

Retrieves all grades for a student in a specific subject.

**Example:**
```python
grades = get_grades_by_student_and_subject(1, 2)
print(f"Found {len(grades)} grade entries for the student in this subject")
for grade in grades:
    print(f"- {grade.date.strftime('%Y-%m-%d')}: {grade.grade}")
```

### `get_average_grade_by_student(student_id: int) -> Optional[float]`

Gets the average grade for a student across all subjects.

**Example:**
```python
avg = get_average_grade_by_student(1)
if avg:
    print(f"Student's average grade: {avg:.2f}")
else:
    print("No grades found for the student")
```

### `get_average_grade_by_subject(subject_id: int) -> Optional[float]`

Gets the average grade for a subject across all students.

**Example:**
```python
avg = get_average_grade_by_subject(1)
if avg:
    print(f"Subject's average grade: {avg:.2f}")
else:
    print("No grades found for the subject")
```

### `get_student_subject_grades_summary(student_id: int) -> Dict[str, Any]`

Gets a summary of grades for a student grouped by subject.

**Example:**
```python
summary = get_student_subject_grades_summary(1)
print("Grade summary by subject:")
for subject, data in summary.items():
    print(f"- {subject}: Average = {data['average']:.2f}")
    print(f"  All grades: {data['grades']}")
```

### `get_recent_grades(limit: int = 10) -> List[Grade]`

Gets the most recent grades.

**Example:**
```python
recent = get_recent_grades(5)  # Get 5 most recent grades
print("Recent grades:")
for grade in recent:
    print(f"- {grade.student.user.first_name} {grade.student.user.last_name}: " +
          f"{grade.subject.name} - {grade.grade} " +
          f"({grade.date.strftime('%Y-%m-%d')})")
```

## Common Patterns and Best Practices

1. **Error Handling**: Most functions return `None` or `False` when an operation fails (e.g., item not found). Always check return values.

2. **Date Handling**: Date strings should be in 'YYYY-MM-DD' format. The utility functions `format_date` and `format_date_to_obj` handle conversions.

3. **Transactions**: All database operations use Flask-SQLAlchemy's session management. Modifications are committed automatically at the end of functions.

4. **Parameter Types**: Be mindful of parameter types. Some functions expect objects (like a Teacher or Subject instance) while others expect IDs.

5. **Soft vs Hard Deletes**: User deletion is implemented as a soft delete (deactivation), while other entities use hard deletes. Consider the implications before deleting data.
