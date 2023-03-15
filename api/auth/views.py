from datetime import datetime
from flask import abort, request
from flask_restx import Namespace, Resource
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_header, get_jwt_identity, current_user

from ..utils import db
from ..models.users import User
from ..models.students import Student
from ..models.teachers import Teacher

from flask_restx import Namespace, fields, marshal

user_namespace = Namespace('Users', description='Namescpace for user and authorization')

user_base_model = user_namespace.model('User Base',{
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True)
})

login_model = user_namespace.model('Login',{
    'email':fields.String(required=True),
    'password':fields.String(required=True)
})

signup_model = user_namespace.model('Signup',{
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'password':fields.String(required=True)
})

student_inline_model = user_namespace.model('student_inline',
    {
    'email': fields.String(),
    'student_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String()
})

teacher_inline_model = user_namespace.model('Teacher Inline',{
    'email': fields.String(),
    'teacher_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String()
})


@user_namespace.route("/register/student")
class StudentCreateView(Resource):
    @user_namespace.expect(signup_model)
    def post(self):
        data = request.get_json()
        if User.query.filter(User.email==data['email']).first():
            abort(409, "A user with that email already exixts")
        student = Student(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], password=pbkdf2_sha256.hash(data['password']))
        student.save()
        student.assign_no()
        return {'message':'Student created',
                'data':user_namespace.marshal(student, student_inline_model)}, 201
    
@user_namespace.route("/register/teacher")
class TeacherCreateView(Resource):
    @user_namespace.expect(signup_model)
    def post(self):
        data = request.get_json()
        if User.query.filter(User.email==data['email']).first():
            abort(409, "A user with that email already exixts")
        teacher = Teacher(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], password=pbkdf2_sha256.hash(data['password']))
        teacher.save()
        teacher.teacher_no=f'ALT/STF/{teacher.id:04d}/{datetime.today().year}'
        teacher.update()
        return {'message':'Teacher created',
                'data':user_namespace.marshal(teacher, teacher_inline_model)}, 201
    
@user_namespace.route("/login")
class LoginView(Resource):
    @user_namespace.expect(login_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.email==data['email']).first()
        if user and pbkdf2_sha256.verify(data['password'], user.password):
            access_token=create_access_token(identity=user.id, additional_claims={user.role:True})
            refresh_token=create_refresh_token(identity=user.id, additional_claims={user.role:True})
            return {
                'user_id': user.id,
                'role':user.role,
                'access_token':access_token, 
                "refresh_token":refresh_token,
                "message":"login successul"
            }
        abort(401, "invalid credentials.")

@user_namespace.route("/refresh")
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user = current_user
        new_token = create_access_token(identity=user,fresh=False, additional_claims={user.role:True})
        jti = get_jwt()['jti']
        return {'access_token':new_token}