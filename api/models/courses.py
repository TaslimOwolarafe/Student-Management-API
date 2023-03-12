from ..utils import db
from datetime import datetime
from .tables import student_course_table


def grader(score):
    if score >= 70: return "A"
    elif score >= 60: return "B"
    elif score >= 50: return "C"
    elif score >= 45: return "D"
    elif score >= 40: return "E"
    else: return "F"

score_points = {
    "A":4, "B":3, "C":2, "D":1, "E":0, "F":0
}


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(40), nullable=True)
    unit = db.Column(db.Integer(), default=0)
    teacher = db.Column(db.Integer(), db.ForeignKey('teachers.id'))
    students = db.relationship("Student", secondary=student_course_table, back_populates="courses", lazy="dynamic") #overlaps="courses"
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)


    def __repr__(self) -> str:
        return f"<Course {self.title}"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

class Grade(db.Model):
    __tablename__ = 'grades'
    __table_args__ = (db.UniqueConstraint('student','course'),)

    id = db.Column(db.Integer(), primary_key=True)
    student = db.Column(db.Integer(), db.ForeignKey('students.id', ondelete='CASCADE'))
    course = db.Column(db.Integer(), db.ForeignKey('courses.id', ondelete='CASCADE'))
    score = db.Column(db.Integer(), nullable=False)
    letter_grade = db.Column(db.String(1), nullable=True)
    student_obj = db.relationship("Student", back_populates="grades")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def save(self):
        self.assign_letter()
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def assign_letter(self):
        self.letter_grade = grader(self.score)
