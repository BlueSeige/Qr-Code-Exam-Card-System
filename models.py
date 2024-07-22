from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Define Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref=db.backref('admin', uselist=False))

    def __repr__(self):
        return f'<Admin {self.user.username}>'

# Define Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    matric_number = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(10), nullable=False)  # Assuming levels like '100L', '200L', etc.

    courses = db.relationship('Course', secondary='student_courses', backref=db.backref('students', lazy='dynamic'))

    user = db.relationship('User', backref=db.backref('student', uselist=False))

    def __repr__(self):
        return f'<Student {self.user.username}>'

# Define Course model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Course {self.code}>'

# Define ExamCard model
class ExamCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    qr_code = db.Column(db.String(200), nullable=False)  # Assuming QR code will be stored as text

    student = db.relationship('Student', backref=db.backref('exam_cards', lazy='dynamic'))

    def __repr__(self):
        return f'<ExamCard {self.id} - Student: {self.student.user.username}>'
