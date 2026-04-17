from utils.whatsapp import send_whatsapp_message

def notify_update(student):
    msg = f"""
    📊 Performance Update

    Name: {student.name}
    Percentage: {student.total_percentage}
    Grade: {student.grade}
    Rank: {student.rank}
    """

    send_whatsapp_message(student.student_whatsapp, msg)
    send_whatsapp_message(student.parent_whatsapp, msg)