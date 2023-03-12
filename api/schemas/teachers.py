from marshmallow import Schema, fields
from .users import UserBaseSchema

class CourseBaseSchema(Schema):
    title = fields.Str(required=True)
    code = fields.Str(required=False)
    unit = fields.Int()

class CourseInlineSchema(CourseBaseSchema):
    id = fields.Int(dump_only=True)

class TeacherBaseSchema(UserBaseSchema):
    id = fields.Int(dump_only=True)
    teacher_no = fields.Str(dump_only=True)

class TeacherRegisterSchema(UserBaseSchema):
    id = fields.Int(dump_only=True)
    password = fields.Str(required=True, load_only=True)

class TeacherSchema(TeacherBaseSchema):
    id = fields.Int(dump_only=True)
    courses = fields.List(fields.Nested(CourseInlineSchema()), dump_only=True)