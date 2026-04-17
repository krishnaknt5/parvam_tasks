from flask import Blueprint, request, redirect
from models.student import add_student
from utils.analytics import total, grade
from utils.ranking import update_ranks
from utils.whatsapp import send_result

student_bp = Blueprint('student', __name__)

@student_bp.route('/add', methods=['POST'])
def add():
    f = request.form

    t = total(f['math'], f['science'], f['english'])
    g = grade(t)

    data = (
        f['name'], f['usn'], f['class'], f['department'],
        f['math'], f['science'], f['english'],
        f['attendance'], f['sports'],
        t, g,
        f['parent_name'], f['parent_whatsapp'], f['student_whatsapp']
    )

    add_student(data)

    update_ranks()

    # WhatsApp trigger
    student_data = {
        "name": f['name'],
        "total": t,
        "grade": g,
        "student_whatsapp": f['student_whatsapp'],
        "parent_whatsapp": f['parent_whatsapp']
    }

    try:
        send_result(student_data)
    except:
        print("WhatsApp not configured")

    return redirect('/dashboard')