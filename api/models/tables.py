from ..utils import db
# from .teachers import Teacher

student_course_table = db.Table(
    "student_course", db.Model.metadata,
    db.Column("student_id", db.String(50), db.ForeignKey(
        "students.id", ondelete='CASCADE')),
    db.Column("course_id", db.String(50), db.ForeignKey(
        "courses.id", ondelete='CASCADE')),
    db.UniqueConstraint("student_id", "course_id",)
)

# teacher_course_table = db.Table(
#     "teacher_course", db.Model.metadata,
#     db.Column("teacher_id", db.String(50), db.ForeignKey(
#         "teachers.id")),
#     db.Column("course_id", db.String(50), db.ForeignKey(
#         "courses.id"))
# )