from ..utils import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    role = db.Column(db.String(25), default='student')

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on': role
        # db.case(
        #     [
        #         (role == "student", "student"),
        #         (role == "teacher", "teacher"),
        #     ],
        #     else_="user"
        # )
    }

    def __repr__(self) -> str:
        return f"<User {self.email}, {self.role}>"