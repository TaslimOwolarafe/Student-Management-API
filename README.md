# Student-management-api

<a name="readme-top"></a>

  ### Table of Contents
  <ul>
    <li><a href="#live-app">Live App</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#technologies-used">Technologies used</a></li>
    <li><a href="#libraries-used">Libraries used</a></li>    
    <li><a href="#to-run-on-your-local-machine">To run on your local machine</a></li>
    <li>
      <a href="#endpoints">Endpoints</a>
      <ol>
        <li><a href="#auth-endpoints">Auth Endpoints</a></li>
        <li><a href="#course-endpoints">Course Endpoints</a></li>
        <li><a href="#student-endpoints">Student Endpoints</a></li>
      </ol>
    </li>
  </ul>
 
### Live app version
Visit [website](https://taslim-student-management.herokuapp.com)
<p align="right"><a href="#readme-top">back to top</a></p>


### About
This is a student management REST api that enables the school authorities(admin) to manage students and allow students to login and check cgpa.
Students have limited access to the app in terms of the number of routes they can access, admin have unlimited access to student and course routes.
The super admin has unlimited access to all routes in the app
<p align="right"><a href="#readme-top">back to top</a></p>


### Technologies Used
- Python
- Flask
- SQLite
 <p align="right"><a href="#readme-top">back to top</a></p>


### Libraries Used
- [Flask restx](https://flask-restx.readthedocs.io/) -  an extension for Flask that adds support for quickly building REST APIs.
- [Flask migrate](https://flask-migrate.readthedocs.io/) - an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - object relational mapper
- [Flask JWT extended](https://flask-jwt-extended.readthedocs.io/en/stable/) - authentication and authorization
<p align="right"><a href="#readme-top">back to top</a></p>


### To run the development environment on your local machine
Clone the repository
```console
git clone https://github.com/TaslimOwolarafe/Student-Management-API
```
Navigate into the project folder
```console
cd {th directory you forked the repo into}
```
Install the required dependencies
```console
pip install -r requirements.txt
```
Intanstiate Database
```console
flask db init
```
```console
flask db migrate
```
```console
flask db upgrade
```

Create a `.env` file or type the following on a bash terminal.
```console
touch .env
```
Copy the code below into the file.
```console
SECRET_KEY=`your secret key`
DEBUG=True
JWT_SECRET_KEY=`another secret key`
```
Save and close the file

Run the Flask app
```console
python app.py
```
 <p align="right"><a href="#readme-top">back to top</a></p>

### To run the Test environment on your local machine
Run pytest in the terminal
```console
pytest
```
 <p align="right"><a href="#readme-top">back to top</a></p>

## Endpoints
#### A brief guide on keywords
- on USER TYPE:
    - "Teacher User" means you have to login with a teacher email and password as these endpoints can only be accessed by teachers. You can generate a teacher token and store for use on any of the endpoints with Teacher User USER TYPE.
    - "Student User" means you have to login with a student email and password as these endpoints can only be accessed by students. You can generate a student token and store for use on any of the endpoints with Student User USER TYPE.
- on Student Primary Key:
    - The Student Primary Key is the "id" of a student and not "student_no" as seen in the list returned from the route "/students/students".

### Auth Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  
| ------- | ----- | ------------ | ------|------- |
|  `/users/register/student` | POST | To register a student account   | Authenticated | Any | 
|  `/users/register/teacher` |  POST | To register a teacher account   | Authenticated| Any | 
|  `/users/login` |  POST  | To authenticate a user   | ---- | Any | 

|  `users/refresh` |  POST  | Generate refresh token  | Authenticated | Any | 

 <p align="right"><a href="#readme-top">back to top</a></p>


### Course Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  VARIABLE RULE | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/courses/courses` |  GET  | Retrieve all courses  | Authenticated | Any | ---- |
|  `/courses/courses` |  POST  | Create a new course   | Authenticated | Teacher User | ---- |
|  `courses/{course_id}` |  GET  | Retrieve a course by an ID, from the list of all courses. Returns course detail and students registered.   | Authenticated | Any | Course ID |
|  `courses/{course_id}/student/{student_id}/registration` |  POST  | Register a student in a course | Authenticated | Teacher User | Course ID, Student ID |
|  `courses/{course_id}/student/{student_id}/registration` |  DELETE  | Unregister a student in a course | Authenticated | Teacher User | Course ID, Student Primary ID |
|  `courses/{course_id}` |  PUT  | Edit a course code or number of units | Authenticated | Teacher User | Course ID |
|  `courses/{course_id}` |  DELETE  | Delete a course by ID | Authenticated | Teacher User | Course ID, Student Primary ID |
|  `courses/{course_id}/registration` |  POST  | for authenticated student user to register a course | Authenticated | Student User | Course ID |
|  `courses/{course_id}/registration` |  DELETE  | for authenticated student user to unregister a course | Authenticated | Student User | Course ID |

 <p align="right"><a href="#readme-top">back to top</a></p>


### Student Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/students/students` |  GET  | Retrieve all students  | Authenticated | Any | ---- |
|  `/students/students/{student_id}` |  GET  | Retrieve a student user by ID, from the list of students, with their registered courses | Authenticated | Any | Student Primary ID |
|  `/students/student` |  GET  | Retrieve authenticated student's detail and courses | Authenticated | Student User | ----- |
|  `/students/students/{student_id}` |  DELETE  | Delete a student by ID | Authenticated | Any | Student ID |
|  `/students/grades/{student_id}` |  GET  | Retrieve a student scores and grades with GPA  | Authenticated | Any | Student Primary ID |
|  `/students/grade` |  GET  | Retrieve authenticated student's scores and grades with GPA  | Authenticated | Student User | ----- |
|  `/students/students/{student_id}` |  PUT  | Edit a student's first_name/last_name/student_no  | Authenticated | Any | ----- |

 <p align="right"><a href="#readme-top">back to top</a></p>

 ### Grades Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/grades/student/{student_id}/course/{course_id}` |  POST  | Grade a student on a course  | Authenticated | Teacher User | Student Primary ID, Course ID |
|  `/grades/student/{student_id}/course/{course_id}` |  GET  | Retrieve a student's grade on a course  | Authenticated | Teacher User | Student Primary ID, Course ID |
|  `/grades/student/{student_id}/course/{course_id}` |  DELETE  | Delete a student's grade on a course  | Authenticated | Teacher User | Student Primary ID, Course ID |
|  `/grades/{course_id}/course` |  GET  | Retrieve the grades of students on a course with ID  | Authenticated | Any | Course ID |

 <p align="right"><a href="#readme-top">back to top</a></p>

 <!-- <p align="right"><a href="#readme-top">back to top</a></p> -->
