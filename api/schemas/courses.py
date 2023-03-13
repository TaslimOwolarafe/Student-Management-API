from flask_restx import fields
from .students import student_inline_model
from .teachers import teacher_inline_model

course_base_model = {
    'title': fields.String(required=True),
    'code': fields.String(),
    'unit': fields.String(),
}

course_model = {
    'id':fields.Integer(),
    'title': fields.String(required=True),
    'code': fields.String(),
    'unit': fields.String(),
    'teacher': fields.Nested(teacher_inline_model),
    'students':fields.List(fields.Nested(student_inline_model))
}
