import os

from flask import Flask
from flask_restx import Api
from .models.users import User
from .models.students import Student
from .models.teachers import Teacher
from .models.courses import Course, Grade
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config.config import config_dict
from .utils import db

from .auth.views import user_namespace
from .students.views import student_namespace
from .courses.views import course_namespace

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)
    # app.config['PROPAGATE_EXCEPTIONS'] = True
    # app.config['API_TITLE'] = "STUDENT MANAGEMENT REST API"
    # app.config['API_VERSION'] = 'V1'
    # app.config['OPENAPI_VERSION'] = '3.0.3'
    # app.config['OPENAPI_URL_PREFIX'] = '/'
    # app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    # app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    db.init_app(app)
    
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()


    migrate = Migrate(app, db, render_as_batch=True)
    api = Api(app,
        title="STUDENT MANAGEMENT API",
        description="SMS",
        authorizations=authorizations,
        security='Bearer Auth')
    
    api.add_namespace(student_namespace)
    api.add_namespace(user_namespace)
    api.add_namespace(course_namespace)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Student': Student,
            'Teacher': Teacher
        }
    
    
    return app