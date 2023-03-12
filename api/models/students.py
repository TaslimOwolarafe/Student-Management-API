from datetime import datetime
from .users import User
from ..utils import db
from .tables import student_course_table

class Student(User):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    student_no = db.Column(db.String(50))
    courses = db.relationship("Course", secondary=student_course_table, back_populates="students") # overlaps="courses"
    grades = db.relationship("Grade", back_populates="student_obj", lazy='dynamic')


    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def save(self):
        db.session.add(self)
        db.session.commit()
        self.student_no = f'ALT/SOE/{self.id:04d}/{datetime.today().year}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def assign_no(self):
        self.student_no = f'ALT/SOE/{self.id:04d}/{datetime.today().year}'
        db.session.commit()