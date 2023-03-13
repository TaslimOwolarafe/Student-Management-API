from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from ..utils import db
from ..models.students import Student
from ..models.courses import Course, Grade

from flask_restx import Resource, Namespace, fields
from http import HTTPStatus


student_namespace = Namespace('students')

course_inline_model = student_namespace.model(
    'Courses', 
    {
        'id': fields.Integer(),
        'title': fields.String(required=True),
        'code': fields.String(),
        'unit': fields.Integer(),
        # 'teacher':fields.String()
    })

student_update_model = student_namespace.model(
    'Student Update', 
    {
        'student_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String()
    })

student_model = student_namespace.model(
    'Student', 
    {
        'id': fields.Integer(),
        'email': fields.String(),
        'student_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String(),
    })

student_inline_model = student_namespace.model('student_inline',
    {
    'email': fields.String(),
    'student_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String()
})

student_course_model = student_namespace.model(
    'Student Courses', 
    {
        'email': fields.String(),
        'student_no': fields.String(),
        'first_name': fields.String(),
        'last_name':fields.String(),
        'courses': fields.Nested(course_inline_model)
    })

course_base_model = student_namespace.model('course_base',{
    'title': fields.String(required=True),
    'code': fields.String(),
    'unit': fields.Integer(),
})


@student_namespace.route("/students/")
class StudentListDetailView(Resource):
    @student_namespace.marshal_with(student_inline_model)
    @student_namespace.doc(description="Get all Students")
    def get(self):
        """
            Get all students.
        """
        students = Student.query.all()
        return students, HTTPStatus.OK
    
@student_namespace.route("/students/<int:student_id>")
class StudentsRetrieveUpdateDestroyView(Resource):
    @student_namespace.response(202, description="Delete a student",
        example={"message":"Student Removed."})
    # @student_namespace.alt_response(404, description="Student not found.")
    @student_namespace.doc(description="Delete a student bt id",
            params= {"student_id":"A student id"})
    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        student.delete()
        return {"message":"Student Removed."}, HTTPStatus.OK

    @student_namespace.marshal_with(student_course_model)
    @student_namespace.doc(description="Retrieve a student with an id.", params= {"student_id":"A student id"})
    def get(self, student_id):
        """
            Retrieve a student and their courses.
        """
        student = Student.query.get_or_404(student_id)
        return student, HTTPStatus.OK
    
    @student_namespace.expect(student_update_model)
    @student_namespace.marshal_with(student_inline_model)
    @student_namespace.doc(description="Update a student by id.", params= {"student_id":"A student id"})
    def put(self, data, student_id):
        """
            Edit a student's first_name/last_name/student_no.
        """
        student = Student.query.get_or_404(student_id)
        student.first_name=data['first_name']
        student.last_name=data['last_name']
        student.student_no=data['student_no']
        db.session.commit()

        return student
    

@student_namespace.route('/student')
class StudentView(Resource):
    @jwt_required()
    @student_namespace.marshal_with(student_course_model)
    @student_namespace.doc(description="Retrive authenticated Student Detail with courses.")
    def get(self):
        """
            Retrieve authenticted Student's details and courses.
        """
        student_id = get_jwt_identity()
        student = Student.query.get_or_404(student_id)

        return student, HTTPStatus.OK
