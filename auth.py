from flask import Flask, request, jsonify
from models import User, db

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.create(username=username, password=password)
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        user = User.get(User.username == username, User.password == password)
        return jsonify({"message": "Login successful!"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "Invalid username or password!"}), 401
