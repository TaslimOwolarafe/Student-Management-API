import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from passlib.hash import pbkdf2_sha256
from ..models.courses import Course
from ..models.students import Student
from ..models.users import User


class CourseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()
        self.app = None
        self.client = None

    def test_student_registeration(self):
        data = {
            'email':'testStudent1@mail.com',
            'first_name':'John',
            'last_name':'Doe',
            'password':pbkdf2_sha256.hash('password')
        }

        response = self.client.post('/users/register/student', json=data)
        assert response.status_code == 201

    def test_teacher_registeration(self):
        data = {
            'email':'testTeacher1@mail.com',
            'first_name':'Bahlil',
            'last_name':'Pratek',
            'password':pbkdf2_sha256.hash('password')
        }
        response = self.client.post('/users/register/teacher', json=data)
        # print(response.get_json())
        # assert response.get_json()['role'] == 'teacher'
        users = User.query.all()
        print(users)
        assert response.status_code == 201
    
    def test_student_login(self):
        data = {
            'email':'testStudent1@mail.com',
            'first_name':'John',
            'last_name':'Doe',
            'password':pbkdf2_sha256.hash('password')
        }
        users = User.query.all()
        print(users)
        self.client.post('/users/register/student', json=data)
        with self.client:
            
            data = {
                'email':'testStudent1@mail.com',
                'password':'password'
            }
            response = self.client.post('/users/login', json=data)
            print(response.get_json())
            assert response.status_code == 200
            # assert response.get_json()['role'] == 'teacher'
            # assert 'access_token' in response.get_json()