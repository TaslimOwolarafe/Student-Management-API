from flask_restx import Namespace, fields


student_namespace = Namespace('student')

course_inline_model = (
    # 'Courses', 
    {
        'id': fields.Integer(),
        'title': fields.String(required=True),
        'code': fields.String(),
        'unit': fields.String(),
    }
)

student_update_model = (
    # 'Student Update', 
    {
        'student_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String()
    }
)

student_model = (
    # 'Student', 
    {
        'id': fields.Integer(),
        'email': fields.String(),
        'student_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String(),
    }
)

student_inline_model = {
    'email': fields.String(),
    'student_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String()
}

student_course_model = (
    # 'Student Courses', 
    {
        'email': fields.String(),
        'student_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String(),
        'courses': fields.Nested(course_inline_model)
    }
)

course_base_model = {
    'title': fields.String(required=True),
    'code': fields.String(),
    'unit': fields.String(),
}


