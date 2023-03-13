from flask_restx import Namespace, fields

user_namespace = Namespace('User', description='Namescpace for user and authorization')

user_base_model = {
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True)
}

login_model = {
    'email':fields.String(required=True),
    'password':fields.String(required=True)
}

signup_model = {
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'password':fields.String(required=True)
}
