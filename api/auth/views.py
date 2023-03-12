from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_header, get_jwt_identity
from ..schemas.students import StudentRegisterSchema, StudentSchema, StudentBaseSchema
from ..schemas.teachers import TeacherRegisterSchema, TeacherBaseSchema
from ..schemas.users import UserLoginSchema

from ..utils import db
from ..models.users import User
from ..models.students import Student
from ..models.teachers import Teacher

blp = Blueprint("Users", 'users', description="Users routes")


@blp.route("/register/student")
class StudentCreateView(MethodView):
    @blp.arguments(StudentRegisterSchema)
    def post(self, data):
        if User.query.filter(User.email==data['email']).first():
            abort(409, message="A user with that email already exixts")
        student = Student(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], password=pbkdf2_sha256.hash(data['password']))
        student.save()
        student.assign_no()
        schema = StudentBaseSchema()
        return {'message':'Student created',
                'data':schema.dump(student)}, 201
    
@blp.route("/register/teacher")
class TeacherCreateView(MethodView):
    @blp.arguments(TeacherRegisterSchema)
    def post(self, data):
        if User.query.filter(User.email==data['email']).first():
            abort(409, message="A user with that email already exixts")
        teacher = Teacher(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], password=pbkdf2_sha256.hash(data['password']))
        teacher.save()
        teacher.teacher_no=f'ALT/STF/{teacher.id:04d}/{datetime.today().year}'
        teacher.update()
        schema = TeacherBaseSchema()
        return {'message':'Teacher created',
                'data':schema.dump(teacher)}
    
@blp.route("/login")
class LoginView(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, data):
        user = User.query.filter(User.email==data['email']).first()
        if user and pbkdf2_sha256.verify(data['password'], user.password):
            access_token=create_access_token(identity=user.id)
            refresh_token=create_refresh_token(identity=user.id)
            return {
                'user_id': user.id,
                'role':user.role,
                'access_token':access_token, 
                "refresh_token":refresh_token,
                "message":"login successul"
            }
        abort(401, message="invalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        jti = get_jwt()['jti']
        return {'access_token':new_token}