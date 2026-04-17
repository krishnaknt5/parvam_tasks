from flask import Blueprint, render_template, session, send_file
from models.student import get_students
from models.db import mysql
from utils.pdf import generate_pdf

dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/dashboard')
def dashboard():
    if session.get('role') == 'admin':
        students = get_students()
        return render_template('admin_dashboard.html', students=students)
    return render_template('student_dashboard.html')


@dash_bp.route('/download/<usn>')
def download(usn):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM students WHERE usn=%s", (usn,))
    s = cur.fetchone()

    if not s:
        return "Student not found"

    # Map DB → dict (based on your table structure)
    student = {
        "name": s[1],
        "usn": s[2],
        "total": s[10],
        "grade": s[11],
        "rank": s[12]
    }

    path = generate_pdf(student)
    return send_file(path, as_attachment=True)