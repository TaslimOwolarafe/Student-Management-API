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
        # 'course':fields.Integer(),
        'letter_grade':fields.String(dump_only=True)
    }
)

@grade_namespace.route("/student/<int:student_id>/course/<int:course_id>")
class GradeStudentCourseGetCreate(Resource):
    @grade_namespace.expect(grade_create)
    @grade_namespace.marshal_with(grade_inline)
    @grade_namespace.doc("Grade a student in a course", params={"student_id":"id of student",'course_id':'id of course'})
    @decorators.teacher_required()
    def post(self, student_id, course_id):
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
    @grade_namespace.doc("Get a student's Grade in a course", params={"student_id":"id of student",'course_id':'id of course'})
    @decorators.teacher_required()
    def get(self, student_id, course_id):
        course = Course.query.get_or_404(course_id)
        student = Student.query.get_or_404(student_id)
        grade = Grade.query.filter_by(student=student.id, course=course.id).first()
        if not grade:
            abort(message=f"Student {student.student_no} has not been graded on {course.code}")
        return grade, HTTPStatus.OK
    

# @grade_namespace.route("/<int:student_id>/courses")
# class GetStudentCoursesGrades(Resource):

