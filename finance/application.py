import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # symbol = [2]
    # name = [3]
    # shares = [2]
    # price = []
    # total = []
    # local = 0
    #
    #
    # items = [{'symbol': "sy"}, {'name': "n"}, {'shares': "sh"}, {'total': "t"}, {'local': "l"}]

    rez1 = []
    rez2 = []
    rez3 = []
    rez4 = []
    rez5 = []
    total2 = 0
    user = db.execute("select username from users where id = :id",
                      id=session.get("user_id"))
    cash = db.execute("select cash from users where id = :id",
                      id=session.get("user_id"))
    users = list(zip(user[0].values()))
    money = list(zip(cash[0].values()))
    ids = db.execute("select id from user_stocks where id_user = :id",
                     id=session.get("user_id"))
    symbol = db.execute("select symbol from user_stocks where id_user = :id",
                        id=session.get("user_id"))
    name = db.execute("select name from user_stocks where id_user = :id",
                      id=session.get("user_id"))
    shares = db.execute("select shares from user_stocks where id_user = :id",
                        id=session.get("user_id"))
    print(symbol)
    item = len(ids)
    for i in symbol:
        for l in i.values():
            rez1.append(l)

    for i in name:
        for l in i.values():
            rez2.append(l)

    for i in shares:
        for l in i.values():
            rez3.append(l)
    for i in rez1:
        rez4.append(lookup(i))
    for l in rez4:
        n, p, s = l.values()
        rez5.append(p)

    # print(rez1)
    print(rez4)
    print(rez5)
    for i in range(item):
        total2 += rez3[i] * rez5[i]
    total2 += money[0][0]
    db.execute("delete from user_stocks where shares=0")
    return render_template("index.html", user=users[0][0], cash=usd(money[0][0]),
                           total=usd(money[0][0]), item=item,
                           a=rez1, b=rez2, c=rez3, y=rez5, total2=usd(total2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing Symbol")

        if not request.form.get("shares"):
            return apology("Missing Shares")

        rez = lookup(request.form.get("symbol"))

        name, price, symbol = rez.values()

        print(name, price, symbol)

        total = price * float(request.form.get("shares"))

        cash = db.execute("select cash from users where id = :id", id=session.get("user_id"))

        print(cash)

        money = list(zip(cash[0].values()))

        cash = money[0][0] - total

        if cash < 0:
            return apology("can't afford")

        db.execute("update users set cash = :cash where id = :id",

                   cash=cash, id=session.get("user_id"))

        db.execute("insert into history(time,user_id,symbol,name,shares,price,total) values (:time, :user_id,:symbol,"

                   ":name, :shares, :price, :total)", time=time.strftime("%d/%m/%Y %X"),

                   user_id=session.get("user_id"), symbol=symbol, name=name,

                   shares=request.form.get("shares"), price=price,

                   total=total)

        verification = db.execute("select id_user, symbol from user_stocks"" where id_user = :id and symbol = :symbol",
                                  id=session.get("user_id"), symbol=symbol)

        if len(verification) != 1:

            db.execute(
                "insert into user_stocks(id_user,symbol,name,shares) values (:id_user, :symbol," ":name, :shares)",
                id_user=session.get("user_id"), symbol=symbol, name=name, shares=request.form.get("shares"))

        else:

            share = db.execute("select shares from user_stocks where id_user=:id and symbol = :symbol",

                               id=session.get("user_id"), symbol=symbol)

            count = list(zip(share[0].values()))

            shares = count[0][0] + int(request.form.get("shares"))

            db.execute("update user_stocks set shares = :shares where id_user = :id and symbol = :symbol",

                       shares=shares, id=session.get("user_id"), symbol=symbol)
        flash("Bought!")

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():  #########
    """Show history of transactions"""

    Symbol = []
    Name = []
    Shares = []
    Price = []
    Transacted = []


    Sy = db.execute("select symbol from history where user_id = :id",
                     id=session.get("user_id"))
    N = db.execute("select name from history where user_id = :id",
                     id=session.get("user_id"))
    Sh = db.execute("select shares from history where user_id = :id",
                     id=session.get("user_id"))
    P = db.execute("select price from history where user_id = :id",
                     id=session.get("user_id"))
    T = db.execute("select time from history where user_id = :id",
                     id=session.get("user_id"))
    ids = db.execute("select id from history where user_id = :id",
                     id=session.get("user_id"))
    item = len(ids)
    for i in Sy:
        for l in i.values():
            Symbol.append(l)
    for i in N:
        for l in i.values():
            Name.append(l)
    for i in Sh:
        for l in i.values():
            Shares.append(l)
    for i in P:
        for l in i.values():
            Price.append(l)
    for i in T:
        for l in i.values():
            Transacted.append(l)

    return render_template("history.html", item = item, a = Symbol, b = Name, c= Shares, e = Price , d = Transacted  )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required  #########
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol")
        if not request.form.get("symbol").isalpha():
            return apology("Symbol must be alphabetical")
        back = lookup(request.form.get("symbol"))
        name, price, symbol = back.values()
        print(name, price, symbol)
        return render_template("quotes.html", name=name, price=price, symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    users = db.execute("select * from users ")
    print(users)
    print(request.method)
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)
        if not request.form.get("confirm"):
            return apology("must provide confirm password", 403)
        if request.form.get("password") != request.form.get("confirm"):
            return apology("confirm password doesn't equal the password")

        check = db.execute("select * from users where username = :username",
                           username=request.form.get("username"))
        print(check)

        if len(check) != 0:
            flash("username busy")
            return redirect("/register")
            # return apology("This username is busy")
        else:
            password_hash = generate_password_hash(request.form.get("password"))
            # ids = db.execute("select id from users")
            print(request.form.get("username"), password_hash)
            db.execute("insert into users(username, hash, cash) values (:username,:hash, :cash)",
                       username=request.form.get("username"), hash=password_hash, cash=10000)
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))
            session["user_id"] = rows[0]["id"]
            print(session["user_id"])
            flash(f"Hello {request.form.get('username')}! Thank you for registration")
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required  ###########
def sell():
    """Sell shares of stock"""
    global named
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing Symbol")

        if not request.form.get("shares"):
            return apology("Missing Shares")

        shares = db.execute("select shares from user_stocks where id_user = :id "
                            "and symbol=:symbol",
                            id=session.get("user_id"),
                            symbol=request.form.get("symbol"))

        for i in shares[0].values():
            shares = i
        print(shares)
        if int(request.form.get("shares")) > shares:
            return apology("To many shares")

        look_price = lookup(request.form.get("symbol"))
        for k, v in look_price.items():
            if k == "price":
                price = v
            if k == "name":
                named = v

        money = price * float(request.form.get("shares"))
        share = shares - int(request.form.get("shares"))

        db.execute("update user_stocks set shares = :shares where id_user = :id"
                   " and symbol = :symbol", shares=share, id=session.get("user_id"),
                   symbol=request.form.get("symbol"))
        cash = db.execute("select cash from users where id = :id", id=session.get("user_id"))
        for i in cash[0].values():
            cash = i

        print(cash)
        user_cash = cash + money
        db.execute("update users set cash = :cash where id = :id",
                   cash=user_cash, id=session.get("user_id"))

        db.execute("insert into history(time,user_id,symbol,name,shares,price,total) values ( :time, :user_id, "
                   ":symbol, :name, "
                   " :shares, :price, :total)", time=time.strftime("%d/%m/%Y %X"),
                   user_id=session.get("user_id"), symbol=request.form.get("symbol"),
                   name=named, shares=-int(request.form.get("shares")), price=price, total=money)

        db.execute("delete from user_stocks where shares=0")
        flash("Sold")
        return redirect("/")

    else:

        rez1 = []
        ids = db.execute("select id from user_stocks where id_user = :id",
                         id=session.get("user_id"))
        symbol = db.execute("select symbol from user_stocks where id_user = :id",
                            id=session.get("user_id"))
        item = len(ids)
        for i in symbol:
            for l in i.values():
                rez1.append(l)

        return render_template("sell.html", item=item, a=rez1)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(port=8080)
