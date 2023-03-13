from flask_restx import Resource, Namespace, fields, abort
from ..models.courses import Course, Grade
from flask import request
from http import HTTPStatus
from ..utils import db, decorators
from ..models.users import User
from ..models.students import Student
from ..models.teachers import Teacher

from flask_jwt_extended import get_jwt_identity, jwt_required, current_user

course_namespace = Namespace("courses", description="Courses Namespace")

teacher_inline = course_namespace.model('teacher_inline',
    {
        'id':fields.Integer(),
        'teacher_no':fields.String(),
        'first_name':fields.String(),
        'last_name':fields.String(),
        'email':fields.String()
    }
    )

course_model = course_namespace.model('course_base',{
    'id':fields.Integer(dump_only=True),
    'title': fields.String(required=True),
    'code': fields.String(),
    'unit': fields.Integer(),
    # 'teacher':fields.Integer()
    'teacher_id':fields.Nested(teacher_inline)

})

course_create = course_namespace.model('course_create',{
    'title': fields.String(required=True),
    'code': fields.String(),
    'unit': fields.Integer(),
})

course_update = course_namespace.model('course_update',{
    'code': fields.String(),
    'unit': fields.Integer(),
})

student_inline_model = course_namespace.model('student_inline',
    {
    'email': fields.String(),
    'student_no': fields.String(),
    'first_name': fields.String(),
    'last_name':fields.String()
})

course_students = course_namespace.model("course_students",
    {
    'id':fields.Integer(dump_only=True),
    'title': fields.String(required=True),
    'code': fields.String(),
    'unit': fields.Integer(),
    'teacher_id':fields.Nested(teacher_inline),
    'students':fields.List(fields.Nested(student_inline_model))
})

student_course_model = course_namespace.model(
    'Student Courses', 
    {
        'email': fields.String(),
        'courses': fields.Nested(course_update)
    })


@course_namespace.route('/courses')
class CourseCreateRetrieve(Resource):
    @course_namespace.expect(course_create)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Create a course")
    @decorators.teacher_required()
    def post(self):
        """
            Create a course.
        """
        teacher = current_user.id
        data = request.get_json()
        course = Course(title=data['title'],code=data['code'],unit=data['unit'],teacher=teacher)
        course.save()
        return course, HTTPStatus.OK
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Get all courses.")
    def get(self):
        """
            Get all courses.
        """
        courses = Course.query.all()
        return courses, HTTPStatus.OK
    
@course_namespace.route('/<int:course_id>')
class CourseDetailUpdateDestroy(Resource):
    @course_namespace.marshal_with(course_students)
    @course_namespace.doc(description="Get a course by id with all students registered.")
    def get(self, course_id):
        """
            Get a course and students.
        """
        course = Course.query.get_or_404(course_id)
        return course, HTTPStatus.OK

    @course_namespace.expect(course_update)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Update a course code and unit by id.", params={'course_id':'A course id.'})
    def put(self, course_id):
        """
            Update course
        """
        course = Course.query.get_or_404(course_id)
        data = request.get_json()
        course.code = data['code']
        course.unit = data['unit']

        return course, HTTPStatus.OK
    
    @course_namespace.doc(description="Delete a course by id")
    def delete(self, course_id):
        """
            delete a course by id
        """
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {'message':'course deleted'}, HTTPStatus.OK

@course_namespace.route("/<int:course_id>/registration")
class StudentCourseRegister(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Register a course for student",params={'course_id':'A course id.'})
    @decorators.student_required()
    def post(self, course_id):
        """
            Register a course
        """
        student = current_user
        course = Course.query.get_or_404(course_id)
        if course in student.courses:
            abort(400, message='course already registred!')
        student.courses.append(course)
        db.session.commit()
        return student.courses, HTTPStatus.OK
    
    @course_namespace.doc(description="Unregister a course for student",params={'course_id':'A course id.'})
    @decorators.student_required()
    def delete(self, course_id):
        """
            Unregister a course
        """
        student = current_user
        course = Course.query.get_or_404(course_id)
        if course not in student.courses:
            abort(400, message='course not registred!')
        student.courses.remove(course)
        db.session.commit()
        return {'message': 'course unregistered', 'data':course_namespace.marshal(student.courses)}, HTTPStatus.OK
    
@course_namespace.route("/<int:course_id>/student/<int:student_id>/registeration")
class StudentRegisteration(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Register a course for student",params={'course_id':'A course id.'})
    def post(self, course_id, student_id):
        """
            Register a course
        """
        student = Student.query.get_or_404(student_id)
        course = Course.query.get_or_404(course_id)
        if course in student.courses:
            abort(400, message='course already registred!')
        student.courses.append(course)
        db.session.commit()
        return student.courses, HTTPStatus.OK
    @course_namespace.doc(description="Unregister a course for student",params={'course_id':'A course id.'})
    def delete(self, course_id, student_id):
        """
            Unregister a course
        """
        student = Student.query.get_or_404(student_id)
        course = Course.query.get_or_404(course_id)
        if course not in student.courses:
            abort(400, message='course not registred!')
        student.courses.remove(course)
        db.session.commit()
        return {'message': 'course unregistered', 'data':course_namespace.marshal(student.courses)}, HTTPStatus.OK