import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from passlib.hash import pbkdf2_sha256
from ..models.courses import Course
from ..models.students import Student


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

    def test_course_registeration(self):
        data = {
            'email':'testStudent1@mail.com',
            'first_name':'John',
            'last_name':'Doe',
            'password':pbkdf2_sha256.hash('password')
        }
        response = self.client.post('/users/register/student', json=data)
        assert response.status_code == 201