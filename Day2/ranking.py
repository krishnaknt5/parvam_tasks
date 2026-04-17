from models.db import mysql

def update_ranks():
    cur = mysql.connection.cursor()

    cur.execute("SELECT id, total FROM students ORDER BY total DESC")
    students = cur.fetchall()

    rank = 1
    for s in students:
        cur.execute(
            "UPDATE students SET rank_position=%s WHERE id=%s",
            (rank, s[0])
        )
        rank += 1

    mysql.connection.commit()