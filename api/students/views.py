from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from ..schemas.students import StudentSchema, StudentUpdateSchema, StudentCourseSchema
from ..utils import db
from ..models.students import Student
from ..models.courses import Course, Grade

blp = Blueprint("students", "STUDENTS", description="Operations on students")

@blp.route("/students/")
class StudentListDetailView(MethodView):
    @blp.response(200, StudentSchema(many=True))
    def get(self):
        students = Student.query.all()
        return students
    
@blp.route("/students/<int:student_id>")
class StudentsRetrieveUpdateDestroyView(MethodView):
    @blp.response(202, description="Delete a student",
        example={"message":"Student Removed."})
    @blp.alt_response(404, description="Student not found.")
    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        student.delete()
        return {"message":"Student Removed."}

    @blp.response(200, StudentSchema, description="Retrieve a student with an id.")
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student
    
    @blp.arguments(StudentUpdateSchema)
    @blp.response(200, StudentSchema)
    def put(self, data, student_id):
        student = Student.query.get_or_404(student_id)
        student.first_name=data['first_name']
        student.last_name=data['last_name']
        student.student_no=data['student_no']
        db.session.commit()

        return student
    

@blp.route('/student')
class StudentView(MethodView):
    @jwt_required()
    @blp.response(200, StudentCourseSchema)
    def get(self):
        student_id = get_jwt_identity()
        student = Student.query.get_or_404(student_id)

        return student