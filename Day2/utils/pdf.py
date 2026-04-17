import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def generate_pdf(student):
    os.makedirs("reports", exist_ok=True)

    file = f"reports/{student['usn']}.pdf"
    doc = SimpleDocTemplate(file)

    elements = []

    elements.append(Paragraph("STUDENT REPORT"))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Name: {student['name']}"))
    elements.append(Paragraph(f"USN: {student['usn']}"))
    elements.append(Paragraph(f"Total: {student['total']}"))
    elements.append(Paragraph(f"Grade: {student['grade']}"))
    elements.append(Paragraph(f"Rank: {student['rank']}"))

    doc.build(elements)

    return file