from marshmallow import Schema, fields
from .students import StudentBaseSchema

class CourseBaseSchema(Schema):
    title = fields.Str(required=True)
    code = fields.Str(required=False)
    unit = fields.Int()

class CourseInlineSchema(CourseBaseSchema):
    id = fields.Int(dump_only=True)

class CourseSchema(CourseBaseSchema):
    id = fields.Int(dump_only=True)
    teacher = fields.Int(dump_only=True)
    students = fields.List(fields.Nested(StudentBaseSchema()), dump_only=True)