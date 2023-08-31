import os
import sqlite3
import re
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from extra import apology, login_required

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

connection = sqlite3.connect("final.db", check_same_thread=False)
cursor = connection.cursor()


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/instructions")
def instructions():
    return render_template("instructions.html")


@app.route("/signup", methods=["GET", "POST"])
def register():

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    email = request.form.get("email")
    program = request.form.get("program")
    grade = request.form.get("grade")

    if request.method == "POST":

        # Ensure username was submitted + no repeat usernames in database
        if not username:
            return apology("must provide username", "ERROR")

        # Ensure password was submitted + matching passwords
        if not password:
            return apology("must provide password", "ERROR")

        elif confirmation != password:
            return apology("passwords do not match", "ERROR")

        # checks emails validity
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email) == None:
            return apology("invalid email", 400)

        # checks grade validity
        if not grade:
            return apology("must provide grade", "ERROR")
        if grade == "":
            return apology("grade must be an integer", 400)
        if grade.isalpha() == True:
            return apology("grade must be an integer", "ERROR")

        if float(grade) % 1 != 0:
            return apology("grade cant be a float", 400)

        if not int(grade):
            return apology("grade must be an integer", 400)
        elif int(grade) <= 0:
            return apology("grade must be a positive integer", 400)
        elif int(grade) < 10 or int(grade) > 12:
            return apology("only accepts highschool students", "ERROR")

        # checks program validity
        if not program:
            return apology("must provide program", "ERROR")

        if program not in ("Partial", "Regular", "Full"):
            return apology("unkown program", "ERROR")

        each_user = cursor.execute("SELECT * FROM users")
        for row in each_user:
            if row[1].strip() == username:
                return apology("username already exists", "ERROR")
            if row[3] == email:
                return apology("email already being used", "ERROR")

        if cursor != None:
            sql = "INSERT INTO users(username, password, email, grade, program) VALUES('{}','{}','{}','{}','{}')".format(username.strip(), generate_password_hash(password), email, grade, program)
            cursor.execute(sql)
            connection.commit()
        else:
            print("cursor is null")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not request.form.get("username"):
            return apology("must provide username", "ERROR")
        elif not request.form.get("password"):
            return apology("must provide password", "ERROR")

        check = cursor.execute("SELECT username FROM users WHERE username = '{}'".format(username))
        all = check.fetchall()
        if len(all) == 0:
            return apology("no account is under this username", "ERROR")

        hash = cursor.execute("SELECT password FROM users WHERE username = '{}'".format(username))
        if check_password_hash(str(hash), password):
            return apology("invalid username and/or password", "ERROR")

        id = cursor.execute("SELECT id FROM users WHERE username = '{}'".format(username))
        for i in id:
            session["user_id"] = i[0]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    tmp = []
    items = []
    allnames = []
    all = cursor.execute("SELECT * FROM users")

    for index, tuples in enumerate(all):

        tmp.append(tuples)
        allnames.append(tuples[1])

        currtupleinfo = {"name": tmp[index][1], "grade": tmp[index][5], "program": tmp[index][6]}
        items.append(currtupleinfo)

    if request.method == "POST":

        name = request.form.get("name")

        if name is None:
            return apology("must select friend's username", "ERROR")

        if name not in allnames:
            return apology("user not found", "ERROR")

        user = cursor.execute("SELECT * FROM users WHERE id = '{}'".format(session["user_id"]))

        newtmp = []
        for row in user:
            newtmp.append(row)

        username = newtmp[0][1]
        password = newtmp[0][2]
        email = newtmp[0][3]
        grade = newtmp[0][5]
        program = newtmp[0][6]

        new = [name]
        cursor.execute("REPLACE INTO users(id, username, password, email, friends, grade, program) VALUES('{}','{}','{}','{}', ?,'{}','{}')".format(int(session["user_id"]), username, password, email, grade, program), new)
        connection.commit()

        return redirect("/")
    else:
        return render_template("add.html", items=items)


@app.route("/table", methods=["GET", "POST"])
@login_required
def table():
    if request.method == "POST":

        day = request.form.get("day")
        if day is None:
            return apology("must select day", "ERROR")

        p1 = request.form.get("period1")
        p2 = request.form.get("period2")
        p3 = request.form.get("period3")
        p4 = request.form.get("period4")

        if p1 is None or p2 is None or p3 is None or p4 is None:
            return apology("all periods must be occupied", "ERROR")

        cursor.execute("REPLACE INTO {}(period_one, period_two, period_three, period_four, userid) VALUES('{}','{}','{}','{}','{}')".format(day, p1.strip(), p2.strip(), p3.strip(), p4.strip(), session["user_id"]))
        connection.commit()

        return render_template("table.html")
    else:
        return render_template("table.html")


@app.route("/summary")
@login_required
def summary():

    for user in cursor.execute("SELECT username FROM users where id = '{}'".format(session["user_id"])):
        users_name = user[0]

    for rows in cursor.execute("SELECT friends FROM users where id = '{}'".format(session["user_id"])):
        friends_name = rows[0]

    for row in cursor.execute("SELECT id FROM users where username = '{}'".format(friends_name)):
        id = row[0]

    day1user = []
    day1friend = []
    day2user = []
    day2friend = []

    for rows1 in cursor.execute("SELECT period_one, period_two, period_three, period_four FROM dayOne where userid = '{}'".format(session["user_id"])):
        day1user = []
        day1user.extend(rows1)

    for rows2 in cursor.execute("SELECT period_one, period_two, period_three, period_four FROM dayOne where userid = '{}'".format(id)):
        day1friend = []
        day1friend.extend(rows2)


    for rows3 in cursor.execute("SELECT period_one, period_two, period_three, period_four FROM dayTwo where userid = '{}'".format(session["user_id"])):
        day2user = []
        day2user.extend(rows3)


    for rows4 in cursor.execute("SELECT period_one, period_two, period_three, period_four FROM dayTwo where userid = '{}'".format(id)):
        day2friend = []
        day2friend.extend(rows4)

    day1user.insert(0, users_name)
    day1friend.insert(0, friends_name)
    day2user.insert(0, users_name)
    day2friend.insert(0, friends_name)

    day1similar = []
    day2similar = []

    for index in range(1, 5):
        tmp = {"period":index, "class":""}
        if day1user[index] == day1friend[index]:
            tmp["class"] = day1user[index]
            day1similar.append(tmp)

        if day2user[index] == day2friend[index]:
            tmp["class"] = day2user[index]
            day2similar.append(tmp)


    return render_template("summary.html", day1user=day1user, day2user=day2user, day1friend=day1friend, day2friend=day2friend, day1similar=day1similar, day2similar=day2similar)
