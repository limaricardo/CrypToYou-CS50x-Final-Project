from flask import session

def add_funds(conn, funds):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET cash = cash + %s WHERE id = %s", (funds, session["user_id"]))
    conn.commit()
    cursor.close()
    return add_funds