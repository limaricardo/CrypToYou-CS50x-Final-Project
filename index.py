from flask import session

def get_crypto_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT crypto_name, symbol, SUM (crypto_owned) AS crypto_owned, ROUND (AVG (price),2) AS average, ROUND (SUM (price * crypto_owned),2) AS total FROM crypto WHERE user_id = %s GROUP BY (crypto_name, symbol) HAVING SUM (crypto_owned) > 0", (session["user_id"],))
    crypto_db = cursor.fetchall()
    cursor.close()
    return crypto_db

def get_cash(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cash FROM users WHERE id = %s", (session["user_id"],))
    cash = cursor.fetchone()
    cursor.close()
    return cash
    
