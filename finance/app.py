import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/cash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "POST":

        amount = int(request.form.get("amount"))

        if not amount:
            return apology("amount must be an integer", 400)
        elif amount <= 0:
            return apology("amount must be a positive integer", 400)

        list_of_user = db.execute("SELECT * FROM users WHERE id = ?", str(session["user_id"]))

        user_id = list_of_user[0]["id"]
        user_username = list_of_user[0]["username"]
        user_hash = list_of_user[0]["hash"]
        user_cash = list_of_user[0]["cash"]

        new_balance = user_cash + amount

        db.execute("REPLACE INTO users (id, username, hash, cash) VALUES(?, ?, ?, ?)",
                   user_id, user_username, user_hash, new_balance)

        return redirect("/")
    else:
        return render_template("cash.html")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    items = []
    seen = []
    sum = 0

    history_list = db.execute("SELECT * FROM history WHERE userid = ?", str(session["user_id"]))
    user_list = db.execute("SELECT * FROM users WHERE id = ?", str(session["user_id"]))

    cash = user_list[0]["cash"]

    for rows in history_list:
        if rows["symbol"] not in seen:
            seen.append(rows["symbol"])

            seen.append(
                {"symbol": rows["symbol"],
                 "name": lookup(rows["symbol"])["name"],
                 "shares": rows["shares"],
                 "price": lookup(rows["symbol"])["price"],
                 "total": rows["shares"] * lookup(rows["symbol"])["price"]}
            )
        else:
            dict_index = seen.index(rows["symbol"]) + 1

            seen[dict_index]["shares"] += rows["shares"]
            seen[dict_index]["total"] += (rows["shares"] * seen[dict_index]["price"])

    items.append(seen[1::2])

    for dictionary in items[0]:
        cash -= dictionary["total"]
        sum += dictionary["total"]

    sum += cash

    return render_template("index.html", items=items[0], cash=cash, sum=sum)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        if shares == "":
            return apology("shares must be an integer", 400)
        if shares.isalpha() == True:
            return apology("shares must be an integer", 400)
        if not lookup(symbol):
            return apology("invalid symbol", 400)
        if float(shares) % 1 != 0:
            return apology("shares cant be a float", 400)
        if not int(shares):
            return apology("shares must be an integer", 400)
        elif int(shares) <= 0:
            return apology("shares must be a positive integer", 400)

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", str(session["user_id"]))[0]
        price = int(lookup(symbol)["price"])

        if user_cash["cash"] - (price * int(shares)) < 0:
            return apology("not enough money", 400)

        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        db.execute("INSERT INTO history (symbol, shares, price, userid, time) VALUES(?,?,?,?,?)",
                   symbol, shares, (price * shares), session["user_id"], time)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = []

    history_list = db.execute("SELECT * FROM history WHERE userid = ?", str(session["user_id"]))

    for r in history_list:
        new = {
            "symbol": r["symbol"],
            "shares": r["shares"],
            "price": lookup(r["symbol"])["price"],
            "time": r["time"]
        }
        rows.append(new)

    return render_template("history.html", items=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forgets any user_id
    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    symbol = request.form.get("symbol")

    if request.method == "POST":

        stock_dict = lookup(symbol)

        if not stock_dict:
            return apology("invalid symbol", 400)

        name = stock_dict["name"]
        symbol = stock_dict["symbol"]
        price = stock_dict["price"]

        return render_template("quoted.html", name=name, symbol=symbol, price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":

        # Ensure username was submitted + no repeat usernames in database
        if not username:
            return apology("must provide username", 400)

        each_user = db.execute('SELECT * FROM users')
        for row in each_user:
            if row["username"] == username:
                return apology("username already exists", 400)

        # Ensure password was submitted + matching passwords
        if not password:
            return apology("must provide password", 400)

        elif confirmation != password:
            return apology("passwords do not match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, generate_password_hash(password))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        history_list = db.execute("SELECT * FROM history WHERE userid = ?", str(session["user_id"]))

        # Code below does the selling
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        if int(shares) <= 0:
            return apology("shares must be positive", 400)

        share_counter = 0
        for dict in history_list:
            if dict["symbol"] == symbol:
                share_counter += dict["shares"]

        if int(shares) > share_counter:
            return apology("not enough shares to sell", 400)

        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        db.execute("INSERT INTO history (symbol, shares, price, userid, time) VALUES (?,?,?,?,?)",
                   symbol, -abs(int(shares)), int(lookup(symbol)["price"]), session["user_id"], time)

        return redirect("/")

    else:
        # Code below gives us the options we have when selling
        history_list = db.execute("SELECT * FROM history WHERE userid = ?", str(session["user_id"]))
        symbols = []
        for row in history_list:
            if row["symbol"] not in symbols:
                symbols.append(row["symbol"])
                symbols.append(row["shares"])
            else:
                symbol_index = symbols.index(row["symbol"])
                symbols[symbol_index + 1] += int(row["shares"])

        numofshares = symbols[1::2]
        options = symbols[::2]
        final = []
        for share in range(0, len(options)):
            if numofshares[share] != 0:
                final.append(options[share])

        return render_template("sell.html", indextable=final)
