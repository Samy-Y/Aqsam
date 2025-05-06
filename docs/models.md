# Models Documentation

This document describes the data models used in the Aqsam application.

## User

Represents a user account in the system.

**Attributes:**

*   `id` (int): Unique identifier for the user.
*   `username` (str): Unique username for the user.
*   `password` (str): Hashed password for the user.
*   `role` (str): Role of the user (e.g., 'admin', 'teacher', 'student', 'writer').
*   `email` (str): User's email address.
*   `first_name` (str): User's first name.
*   `last_name` (str): User's last name.
*   `birth_date` (date): User's birth date.
*   `phone_number` (str): User's phone number.
*   `profile_picture_filename` (str): Filename of the user's profile picture. Stored in static/assets/profile_pictures.
*   `email_verified` (bool): Indicates if the user's email is verified.
*   `email_verification_token` (str): Token for email verification.
*   `email_verification_expiry` (datetime): Expiry time for the email verification token.
*   `password_reset_token` (str): Token for password reset.
*   `password_reset_expiry` (datetime): Expiry time for the password reset token.
*   `activated` (bool): Indicates if the user's account is activated.

**Relationships:**

*   `student` (Student): One-to-one relationship with the Student model.
*   `teacher` (Teacher): One-to-one relationship with the Teacher model.
*   `writer` (Writer): One-to-one relationship with the Writer model.

## Student

Represents a student in the system.

**Attributes:**

*   `id` (int): Unique identifier for the student (foreign key to User).
*   `class_id` (int): Identifier for the class the student is enrolled in (foreign key to Class).

**Relationships:**

*   `user` (User): One-to-one relationship with the User model.
*   `class_` (Class): Many-to-one relationship with the Class model.
*   `grades` (Grade): One-to-many relationship with the Grade model.

## Teacher

Represents a teacher in the system.

**Attributes:**

*   `id` (int): Unique identifier for the teacher (foreign key to User).

**Relationships:**

*   `subjects` (list of Subject): Many-to-many relationship with the Subject model.
*   `classes` (list of Class): Many-to-many relationship with the Class model.
*   `grades` (list of Grade): One-to-many relationship with the Grade model.
*   `user` (User): One-to-one relationship with the User model.

## Class

Represents a class or grade level.

**Attributes:**

*   `id` (int): Unique identifier for the class.
*   `name` (str): Name of the class (e.g., "A").
*   `level` (str): Grade level (e.g., "3rd Year").

**Relationships:**

*   `students` (list of Student): One-to-many relationship with the Student model.
*   `teachers` (list of Teacher): Many-to-many relationship with the Teacher model.

## Subject

Represents a subject.

**Attributes:**

*   `id` (int): Unique identifier for the subject.
*   `name` (str): Name of the subject.

**Relationships:**

*   `teachers` (list of Teacher): Many-to-many relationship with the Teacher model.
*   `grades` (list of Grade): One-to-many relationship with the Grade model.

## Grade

Represents a student's grade in a subject.

**Attributes:**

*   `id` (int): Unique identifier for the grade.
*   `student_id` (int): Foreign key referencing the student.
*   `subject_id` (int): Foreign key referencing the subject.
*   `teacher_id` (int): Foreign key referencing the teacher.
*   `grade` (float): The grade value.
*   `date` (datetime): The date when the grade was assigned.
*   `comment` (str): Optional comment about the grade.

**Relationships:**

*   `student` (Student): Many-to-one relationship with the Student model.
*   `subject` (Subject): Many-to-one relationship with the Subject model.
*   `teacher` (Teacher): Many-to-one relationship with the Teacher model.

## Writer

Represents a writer in the system.

**Attributes:**

*   `id` (int): Unique identifier for the writer (foreign key to User).

**Relationships:**

*   `user` (User): One-to-one relationship with the User model.
*   `articles` (list of Article): One-to-many relationship with the Article model.

## Article

Represents an article written by a writer.

**Attributes:**

*   `id` (int): Unique identifier for the article.
*   `title` (str): Title of the article.
*   `author_id` (int): ID of the author (writer).
*   `content_md` (str): Content of the article in Markdown format.
*   `created_at` (datetime): Timestamp when the article was created.
*   `last_edited` (datetime): Timestamp when the article was last edited.
*   `is_published` (bool): Flag indicating if the article is published.

**Relationships:**

*   `author` (Writer): Many-to-one relationship with the Writer model.
