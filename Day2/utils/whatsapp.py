from twilio.rest import Client
import os

def send_result(student):
    try:
        client = Client(
            os.getenv("TWILIO_SID"),
            os.getenv("TWILIO_AUTH")
        )

        msg = f"""Result Updated 📊
Name: {student['name']}
Total: {student['total']}
Grade: {student['grade']}"""

        from_whatsapp = os.getenv("TWILIO_WHATSAPP")

        # ✅ Format numbers correctly
        student_no = f"whatsapp:+91{student['student_whatsapp']}"
        parent_no = f"whatsapp:+91{student['parent_whatsapp']}"

        # Send to student
        client.messages.create(
            body=msg,
            from_=from_whatsapp,
            to=student_no
        )

        # Send to parent
        client.messages.create(
            body=msg,
            from_=from_whatsapp,
            to=parent_no
        )

        print("✅ WhatsApp sent successfully")

    except Exception as e:
        print("❌ WhatsApp Error:", e)