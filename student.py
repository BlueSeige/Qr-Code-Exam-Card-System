from flask import request, jsonify, session
from models import Course, ExamCard, Student, User

def init_student_routes(app):
    @app.route('/student/register_course', methods=['POST'])
    def register_course():
        if 'user_id' not in session or session.get('is_admin'):
            return jsonify({'error': 'Unauthorized access'}), 403

        data = request.get_json()
        course_code = data['course_code']

        try:
            course = Course.get(Course.course_code == course_code)
            student = Student.select().join(User).where(User.id == session['user_id']).first()
            if not student:
                return jsonify({'error': 'User is not registered as a student'}), 400

            ExamCard.create(student=student, course=course, qr_code='')  # QR code will be generated later
            return jsonify({'message': 'Course registration successful'}), 201
        except Course.DoesNotExist:
            return jsonify({'error': 'Course not found'}), 404

    @app.route('/student/courses', methods=['GET'])
    def get_student_courses():
        if 'user_id' not in session or session.get('is_admin'):
            return jsonify({'error': 'Unauthorized access'}), 403

        student = Student.select().join(User).where(User.id == session['user_id']).first()
        if not student:
            return jsonify({'error': 'User is not registered as a student'}), 400

        exam_cards = [{'id': ec.id, 'course': {'id': ec.course.id, 'course_code': ec.course.course_code, 'course_name': ec.course.course_name}} for ec in student.exam_cards]
        return jsonify(exam_cards), 200
