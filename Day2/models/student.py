from models.db import mysql

def add_student(data):
    cur = mysql.connection.cursor()
    cur.execute("""
    INSERT INTO students(
    name,usn,class,department,
    math,science,english,
    attendance,sports,total,grade,
    parent_name,parent_whatsapp,student_whatsapp)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, data)
    mysql.connection.commit()

def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    return cur.fetchall()