import os
import psycopg2
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, error_login, error_register, lookup, error_trade, get_history, calculate_ImpLoss, error_calculator, error_quoted, error_addFunds
from trade import get_total_shares, sell, buy, get_user
from index import get_cash, get_crypto_db
from addFunds import add_funds


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()


@app.route("/")
def index():
    if session.get("user_id") is None:
        return redirect("/calculator")
    elif session.get("user_id"):
        crypto_db = get_crypto_db(conn)
        cash = get_cash(conn)
        return render_template("index.html", crypto_db = crypto_db, cash = cash)

@app.route("/register", methods=["GET", "POST"])
def register():
    #Register User
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        if not username:
            return error_register("Must provide a username")
        elif not request.form.get("password"):
            return error_register("Must provide password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return error_register("Password don't match")
        elif cursor.fetchone() is not None:
            return error_register("Username already taken")


        cursor.execute("INSERT INTO users (username, hash) VALUES(%s, %s)", (username, password))
        conn.commit()
    
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    #Log user in
    
    #Forget any user id
    session.clear()
    
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        
        #Ensure users was submitted
        if not request.form.get("username"):
            return error_login("Must provide a username")
        
        #Ensure password was submitted
        elif not request.form.get("password"):
            return error_login("Must provide a password")

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        check = cursor.fetchone()
        
        if check is None or not check_password_hash(check[2], request.form.get("password")):
            return error_login("Invalid username and/or password")

        session["user_id"] = check[0]

        return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    
    elif request.method == "POST":
        symbol = request.form.get("symbol").upper()
        result = lookup(symbol)
        if result == "" or result == None:
            return error_quoted("The token did not exist on our Database.")
        else:
            return render_template("quoted.html", result = result)
        
        

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    
    # Redirect user to login form
    return redirect("/")

@app.route("/trade", methods=["GET", "POST"])
@login_required
def trade():
    if request.method == "GET":
        return render_template("trade.html")
    
    elif request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares", type=int)
        result = lookup(symbol)
        user = get_user(conn)    
        total_shares = get_total_shares(conn, symbol)
        
        
        # Conditions for method "POST" in general
        if symbol == "":
            return error_trade("You should input a token symbol.")
        
        elif result == None:
            return error_trade("The token did not exist on our Database.")
        
        elif shares == None or shares < 1:
            return error_trade("You should input a positive number.")

        # Conditions when Buying crypto
        elif request.form.get("action") == "Buy":
            if user[0] < (result["price"] * shares):
                return error_trade("You can not afford the number of crypto stock at the current price.")
            else:
                buy(conn, result, shares)       
                return redirect("/")
        elif request.form.get("action") == "Sell":
            if total_shares == None or shares > total_shares[2]:
                print(total_shares)
                return error_trade("You don't have enough crypto stock to sell.")
            else:
                sell(conn,result, shares)
                return redirect("/")

@app.route("/history")
@login_required
def history():
    #Show history of transactions
    history_transac = get_history(conn)
    return render_template("history.html", history_transac = history_transac)


@app.route("/addFunds", methods=["GET", "POST"])
@login_required
def addFunds():
    if request.method == "GET":
        return render_template("addFunds.html")

    if request.method == "POST":
        funds = request.form.get("funds", type = int)

        if funds == None or funds <= 0:
            return error_addFunds("You should input a positive number.")

        add_funds(conn, funds)
        return redirect("/")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "GET":
        return render_template("calculator.html")
    
    if request.method == "POST": 

        priceChange1 = request.form.get("priceChange1", type=float)
        priceChange2 = request.form.get("priceChange2", type=float)
        poolWeight1 = request.form.get("poolWeight1", type=float)
        poolWeight2 = request.form.get("poolWeight2", type=float)

        impermanentLoss = calculate_ImpLoss(priceChange1, priceChange2, poolWeight1, poolWeight2)

        if impermanentLoss == 1: 
            return error_calculator("Number must be positive into 'Price Change' and 'Pool Weight'. ")
        if impermanentLoss == 2:
            return error_calculator("The sum of pool weight must be 100%.")

        return render_template("calculator.html", impermanentLoss = impermanentLoss)



if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

# @app.route("/login", methods=["GET", "POST"])
# @login_required
# def login():
#     #Query database for username
#     rows = conn.execute("SELECT")
