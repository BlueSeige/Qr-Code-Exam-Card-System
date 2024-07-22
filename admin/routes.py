from flask import Blueprint, jsonify, request

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    # Implement course creation logic here
    return jsonify({"message": "Course added successfully!"}), 201

@admin_bp.route('/courses', methods=['GET'])
def list_courses():
    # Implement course listing logic here
    return jsonify({"message": "List of courses"}), 200
