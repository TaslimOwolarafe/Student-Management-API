from marshmallow import Schema, fields
from .users import UserBaseSchema
from flask_restx import Namespace, fields

class CourseBaseSchema(Schema):
    title = fields.Str(required=True)
    code = fields.Str(required=False)
    unit = fields.Int()

class CourseInlineSchema(CourseBaseSchema):
    id = fields.Int(dump_only=True)


class StudentBaseSchema(UserBaseSchema):
    id = fields.Int(dump_only=True)
    student_no = fields.Str(dump_only=True)

class StudentRegisterSchema(UserBaseSchema):
    id = fields.Int(dump_only=True)
    password = fields.Str(required=True, load_only=True)

class StudentSchema(StudentBaseSchema):
    id = fields.Int(dump_only=True)

class StudentCourseSchema(StudentSchema):
    courses = fields.List(fields.Nested(CourseInlineSchema()), dump_only=True)

class StudentUpdateSchema(Schema):
    student_no = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()

# student_namespace = Namespace('student')

# student_update_model = student_namespace.model(
#     'Student Update', {
#         'student_no': fields.String(),
#         'first_name': fields.String(),
#         'last_name':fields.String()
#     }
# )

# student_course_model = student_namespace.model(
#     'Student Courses', {
        
#     }
# )
