from models.db import mysql

def create_user(name,email,password,role):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",
        (name,email,password,role)
    )
    mysql.connection.commit()

def get_user(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s",(email,))
    return cur.fetchone()