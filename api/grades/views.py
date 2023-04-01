from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from ..utils import db, decorators
from ..models.students import Student
from ..models.courses import Course, Grade

from flask_restx import Resource, Namespace, fields, abort
from http import HTTPStatus

grade_namespace = Namespace('grades', description="Operation on grades and results.")

grade_model = grade_namespace.model(
    'Grade', {
        'id':fields.String(dump_only=True),
        'student':fields.Integer(),
        'course':fields.Integer(),
        'score':fields.Integer(),
        'letter_grade':fields.String()   
    })

grade_create = grade_namespace.model(
    "Grade Create", {
        'score':fields.Integer(required=True),
    }
)

student_inline_model = grade_namespace.model('student_inline',
    {
    'email': fields.String(),
    'student_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String()
})

course_inline_model = grade_namespace.model(
    'Courses', 
    {
        'id': fields.Integer(),
        'title': fields.String(required=True),
        'unit': fields.Integer(),
    })

grade_inline = grade_namespace.model(
    'Grade Inline', {
        'score':fields.Integer(required=True),
        'student_obj':fields.Nested(student_inline_model, dump_only=True),
        'course_obj':fields.Nested(course_inline_model, dump_only=True),
        'letter_grade':fields.String(dump_only=True)
    }
)

grade = grade_namespace.model(
    'grade', {
        'score':fields.Integer(),
        'letter_grade':fields.String(),
        'student_obj':fields.Nested(student_inline_model)
    }
)

grade_update = grade_namespace.model('grade update',
    {
        'score': fields.Integer(),
    })

course_grade = grade_namespace.model('Course Grades',
    {
        'id':fields.Integer(),
        'title':fields.String(),
        'unit':fields.Integer(),
        'grades':fields.List(fields.Nested(grade))
    })

@grade_namespace.route("/student/<int:student_id>/course/<int:course_id>")
class GradeStudentCourseGetCreate(Resource):
    @grade_namespace.expect(grade_create)
    @grade_namespace.marshal_with(grade_inline)
    @grade_namespace.doc(description="Grade a student in a course", params={"student_id":"id of student",'course_id':'id of course'})
    @jwt_required()
    @decorators.teacher_required()
    def post(self, student_id, course_id):
        """
            Grade a student on a course.
        """
        data = request.get_json()
        course = Course.query.get_or_404(course_id)
        student = Student.query.get_or_404(student_id)
        ex_grade = Grade.query.filter_by(student=student.id, course=course.id).first()
        if ex_grade:
            abort(400, message="Student has already been graded on this course.")
        if course not in student.courses:
            abort(400, message="Course not registred on student.")
        grade = Grade(student=student.id, course=course.id, score=data['score'])
        grade.save()
        return grade, HTTPStatus.OK
    
    @grade_namespace.marshal_with(grade_inline)
    @grade_namespace.doc(description="Get a student's Grade in a course", params={"student_id":"id of student",'course_id':'id of course'})
    @jwt_required()
    @decorators.teacher_required()
    def get(self, student_id, course_id):
        """
            Teacher user authentication required.
        """
        course = Course.query.get_or_404(course_id)
        student = Student.query.get_or_404(student_id)
        grade = Grade.query.filter_by(student=student.id, course=course.id).first()
        if not grade:
            abort(400, message=f"Student {student.student_no} has not been graded on {course.code}")
        return grade, HTTPStatus.OK

    @grade_namespace.expect(grade_update)
    @grade_namespace.marshal_with(grade_inline)
    @grade_namespace.doc(description="Edit a student with student_id, score on course with course_id")
    def put(self, student_id, course_id):
        """
            Teacher user authentication required.
            Edit a student's score on a course.
        """
        data = request.get_json()
        course = Course.query.get_or_404(course_id)
        student = Student.query.get_or_404(student_id)
        grade = Grade.query.filter_by(student=student.id, course=course.id).first()
        if not grade:
            abort(400, message=f"Student {student.student_no} has not been graded on {course.code}")
        grade.score = data['score']
        grade.update()
        return grade, HTTPStatus.OK
    
    @grade_namespace.doc(params={"student_id":"id of student", "course_id":"id of course"}, description="Delete a grade of a student on a course.")
    @jwt_required()
    @decorators.teacher_required()
    def delete(self, student_id, course_id):
        """
            Delete a students grade on a course.
            Teacher user authentication required.
        """
        course = Course.query.get_or_404(course_id)
        student = Student.query.get_or_404(student_id)
        grade = Grade.query.filter_by(student=student.id, course=course.id).first()
        if not grade:
            abort(400, message=f"Student {student.student_no} has not been graded on {course.code}")
        db.session.delete(grade)
        return {'message':'grade deleted'}, HTTPStatus.OK


@grade_namespace.route("/<int:course_id>/course")
class GetCourseStudentGrades(Resource):
    @grade_namespace.doc(description="Get students grades in a particular course.")
    def get(self, course_id):
        """
            Get grades of students in a course with course_id.
        """
        course = Course.query.get_or_404(course_id)
        course_students = course.students
        ungraded_students = [student for student in course_students if Grade.query.filter_by(course=course.id, student=student.id).first()==None]
        data = grade_namespace.marshal(course, course_grade)
        data.update({'ungraded_students':grade_namespace.marshal(ungraded_students, student_inline_model)})
        return data, HTTPStatus.OK

