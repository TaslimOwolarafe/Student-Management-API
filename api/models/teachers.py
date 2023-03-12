from datetime import datetime
from .users import User
from ..utils import db

class Teacher(User):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    teacher_no = db.Column(db.String(50))
    courses = db.relationship("Course", backref="teacher_id", lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    def save(self):
        db.session.add(self)
        db.session.commit()
        self.student_no = f'ALT/STF/{self.id:04d}/{datetime.today().year}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def assign_no(self):
        self.student_no = f'ALT/STF/{self.id:04d}/{datetime.today().year}'
        db.session.commit()

    def update(self):
        db.session.commit()