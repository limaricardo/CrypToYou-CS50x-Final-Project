from flask import session

def buy(conn, result, shares):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO crypto (user_id, crypto_owned, price, symbol, crypto_name) VALUES (%s, %s, %s, %s, %s)", (session["user_id"], shares, result["price"], result["symbol"], result["name"]))
    cursor.execute("UPDATE users SET cash = cash - %s WHERE id = %s", (result["price"] * shares, session["user_id"]))
    conn.commit() 
    cursor.close()

def get_user(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cash FROM users WHERE id = %s", (session["user_id"],))
    user = cursor.fetchone()
    cursor.close()
    return user

def sell(conn, result, shares ):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO crypto (user_id, crypto_owned, price, symbol, crypto_name) VALUES (%s, %s, %s, %s, %s)", ((session["user_id"]), -shares, result["price"], result["symbol"], result["name"]))
    cursor.execute("UPDATE users SET cash = cash + %s WHERE id = %s", (result["price"] * shares, session["user_id"]))
    conn.commit() 
    cursor.close()

def get_total_shares(conn, symbol):
    cursor = conn.cursor()
    cursor.execute("SELECT crypto_name, symbol, SUM (crypto_owned) AS crypto_owned, ROUND (AVG (price),2) AS average, ROUND (SUM (price * crypto_owned),2) AS total FROM crypto WHERE user_id = %s and symbol = %s GROUP BY (crypto_name, symbol) HAVING SUM (crypto_owned) > 0", (session["user_id"], symbol))
    total_shares = cursor.fetchone()
    cursor.close()
    return total_shares
