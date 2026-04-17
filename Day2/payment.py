from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))  # student / admin
    whatsapp = db.Column(db.String(15))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    usn = db.Column(db.String(50), unique=True)
    year = db.Column(db.String(20))
    department = db.Column(db.String(50))

    math = db.Column(db.Float)
    science = db.Column(db.Float)
    english = db.Column(db.Float)

    attendance = db.Column(db.Float)
    sports = db.Column(db.Float)

    total_percentage = db.Column(db.Float)
    grade = db.Column(db.String(5))
    rank = db.Column(db.Integer)

    parent_name = db.Column(db.String(100))
    parent_whatsapp = db.Column(db.String(15))
    student_whatsapp = db.Column(db.String(15))