from flask import Flask, request, jsonify
from models import Course, Admin, Student, User, ExamCard, db
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    course_code = data['course_code']
    course_name = data['course_name']
    department = data['department']
    new_course = Course(course_code=course_code, course_name=course_name, department=department)
    new_course.save()
    return jsonify({"message": "Course added successfully!"}), 201

@app.route('/courses', methods=['DELETE'])
def remove_course():
    data = request.get_json()
    course_code = data['course_code']
    course = Course.get(Course.course_code == course_code)
    course.delete_instance()
    return jsonify({"message": "Course deleted successfully!"}), 200

@app.route('/courses', methods=['GET'])
def list_courses():
    courses = Course.select()
    course_list = []
    for course in courses:
        course_list.append({
            "course_code": course.course_code,
            "course_name": course.course_name,
            "department": course.department
        })
    return jsonify(course_list), 200

@app.route('/departments', methods=['POST'])
def add_department():
    data = request.get_json()
    department = data['department']
    new_department = Course(department=department)
    new_department.save()
    return jsonify({"message": "Department added successfully!"}), 201

@app.route('/departments', methods=['DELETE'])
def remove_department():
    data = request.get_json()
    department = data['department']
    query = Course.delete().where(Course.department == department)
    query.execute()
    return jsonify({"message": "Department deleted successfully!"}), 200

@app.route('/admins', methods=['POST'])
def create_admin():
    data = request.get_json()
    username = data['username']
    password = data['password']
    new_admin = Admin.create(username=username, password=password)
    return jsonify({"message": "Admin added successfully!"}), 201

@app.route('/students', methods=['POST'])
def register_student():
    data = request.get_json()
    user = User.create(username=data['username'], password=data['password'])
    student = Student.create(
        user=user,
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=data['date_of_birth'],
        matric_number=data['matric_number'],
        department=data['department'],
        level=data['level']
    )
    return jsonify({"message": "Student registered successfully!"}), 201

@app.route('/exam-cards', methods=['POST'])
def generate_exam_card():
    data = request.get_json()
    student = Student.get(Student.id == data['student_id'])
    course = Course.get(Course.id == data['course_id'])
    qr_code_data = f"{student.first_name},{student.last_name},{student.date_of_birth},{student.matric_number},{student.department},{student.level},{course.course_code},{course.course_name}"

    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Convert QR Code to Base64 string
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    exam_card = ExamCard.create(student=student, course=course, qr_code=qr_code_str)
    return jsonify({"message": "Exam card generated successfully!", "qr_code": qr_code_str}), 201
