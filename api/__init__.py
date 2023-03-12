import os

from flask import Flask
from flask_smorest import Api
from .models.users import User
from .models.students import Student
from .models.teachers import Teacher
from .models.courses import Course, Grade
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config.config import config_dict
from .utils import db

from .auth.views import blp as AuthBlp
from .students.views import blp as StudentBlp

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "STUDENT MANAGEMENT REST API"
    app.config['API_VERSION'] = 'V1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)
    
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    jwt = JWTManager(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Student': Student,
            'Teacher': Teacher
        }
    
    api.register_blueprint(AuthBlp, url_prefix="/students/")
    api.register_blueprint(StudentBlp)
    
    return app