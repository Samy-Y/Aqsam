from app import db

teacher_subject = db.Table(
    "teacher_subject",
    db.Column("teacher_id", db.Integer, db.ForeignKey("teacher.id"), primary_key=True),
    db.Column("subject_id", db.Integer, db.ForeignKey("subject.id"), primary_key=True)
)

teacher_class = db.Table(
    "teacher_class",
    db.Column("teacher_id", db.Integer, db.ForeignKey("teacher.id"), primary_key=True),
    db.Column("class_id",   db.Integer, db.ForeignKey("class.id"),   primary_key=True)
)

teacher_grades = db.Table(
    "teacher_grades",
    db.Column("teacher_id", db.Integer, db.ForeignKey("teacher.id"), primary_key=True),
    db.Column("grade_id",   db.Integer, db.ForeignKey("grade.id"),   primary_key=True)
)