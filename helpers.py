import os
import json
from requests import Session
import json
from flask import redirect, render_template, session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error_login(message):
    return render_template("login.html", error = message)

def error_register(message):
    return render_template("register.html", error = message)

def error_trade(message):
    return render_template("trade.html", error = message)

def error_calculator(message):
    return render_template("calculator.html", error = message)

def error_quoted(message):
    return render_template("quote.html", error = message)

def error_addFunds(message):
    return render_template("addFunds.html", error = message)

def lookup(symbol):
    url = os.environ['API_URL']

    parameters = {
        'convert':'USD',
        'symbol': symbol
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ['API_KEY']
    }


    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return {
            "name": data["data"][symbol]["name"],
            "symbol": data["data"][symbol]["symbol"],
            "total_supply": "{:,.2f}".format(data["data"][symbol]["total_supply"]),
            "max_supply": "{:,.2f}".format(data["data"][symbol]["max_supply"]),
            "cmc_rank": data["data"][symbol]["cmc_rank"],
            "price": float(data["data"][symbol]["quote"]["USD"]["price"]),
            "market_cap": "{:,.2f}".format(float(data["data"][symbol]["quote"]["USD"]["market_cap"]))
            
        }
    except:
        return None

def get_history(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crypto WHERE user_id = %s", (session["user_id"],))
    history = cursor.fetchall()
    cursor.close()
    return history

def calculate_ImpLoss(priceChange1, priceChange2, poolWeight1, poolWeight2):
    if priceChange1 == None or priceChange2 == None or poolWeight1 == None or poolWeight2 == None:
        return 1

    if priceChange1 == 0 and priceChange2 == 0 and poolWeight1 == 0 and poolWeight2 == 0 or (poolWeight1 == 0 and poolWeight2 == 0):
        return 1

    asset1 = (priceChange1 / 100) + 1  
    asset2 = (priceChange2 / 100) + 1  
    valueOfPool = (asset1 ** (poolWeight1 / 100)) * (asset2 ** (poolWeight2 / 100)) 
    valueIfHeld = ((asset1 * poolWeight1)/100) + ((asset2 * poolWeight2)/ 100)
    impermanentLoss = "{:,.2f}".format(((valueOfPool / valueIfHeld) - 1) * (-100))
    
    return impermanentLoss
    
     

