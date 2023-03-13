from flask_restx import Namespace, fields

course_inline_model = (
    # 'Courses', 
    {
        'id': fields.Integer(),
        'title': fields.String(required=True),
        'code': fields.String(),
        'unit': fields.String(),
    }
)

teacher_model = {
    'id': fields.Integer(),
    'email': fields.String(),
    'student_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String(),
}

teacher_update_model = (
    # 'teacher Update', 
    {
        'teacher_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String()
    }
)

teacher_model = (
    # 'teacher', 
    {
        'id': fields.Integer(),
        'email': fields.String(),
        'teacher_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String(),
    }
)

teacher_inline_model = {
    'email': fields.String(),
    'teacher_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String()
}

teacher_course_model = (
    # 'teacher Courses', 
    {
        'email': fields.String(),
        'teacher_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String(),
        'courses': fields.Nested(course_inline_model)
    }
)