from flask import Flask, render_template, request, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import datetime
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
@app.route('/home')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM category''')
    category_data = c.fetchall()
    conn.commit()
    conn.close()
    if "user_id" not in session:
        return render_template("home.html", category=category_data)
    if len(session) > 0:
        user = session["user_id"]
        return render_template("home.html", category=category_data, user=user)



@app.route('/prod_cat1', methods=["GET", "POST"])
def category():
    categ = request.form.get("categ")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM productos WHERE category = (?)''', (categ,))
    prod_data = c.fetchall()
    conn.commit()
    conn.close()
    return render_template("cat1.html", productos=prod_data)


@app.route('/prod', methods=["POST"])
def prod():
    idd = request.form.get("id")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM productos WHERE productID = (?)''', (idd,))
    prod_data = c.fetchall()
    conn.commit()
    conn.close()
    return render_template("single_prod.html", prod_data=prod_data)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registration.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return "Name missing!!"
        if not password:
            return "Name password!!"

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT INTO users (username, hash) VALUES(?, ?)''', (username, generate_password_hash(password),))
            user_data = c.fetchall()
            conn.commit()
            conn.close()
        except NameError:
            return"existe"
        session["user_id"] = user_data[0][0]
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    if request.method == "POST":
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        user = c.fetchall()
        conn.commit()
        conn.close()
        if len(user) != 1 or not check_password_hash(user[0][2], request.form.get("password")):
            return "invalid username and/or password"
        session["user_id"] = user[0][0]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")


def logout():


    session.clear()
    return redirect("/")


@app.route("/cart", methods=["GET", "POST"])
def cart():

    if "cart" not in session:
        session["cart"] = []
    if request.method == "POST":
        idd = request.form.get("id")

        if idd:
            session["cart"].append(idd)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    list_dict =[]
    # create user cart tab
    x = session["user_id"]
    c.execute('''CREATE TABLE IF NOT EXISTS "%s"
                  ( product_name TEXT, qty INTEGER, price REAL)''' % x)
    for producto in session["cart"]:
        c.execute('''SELECT * FROM productos WHERE productID IN (?)''', (producto,))
        user_cart = c.fetchall()
    #insert values into user cart tab
        c.execute('''INSERT INTO "%s"( product_name, qty,price)
                         VALUES (?,?,?)''' % x, (user_cart[0][1], request.form.get("quantity"), user_cart[0][2],))
        c.execute('''SELECT * FROM "%s" WHERE product_name == (?)'''% x, ( user_cart[0][1],))
        thiscart = c.fetchall()
        dict_prod = {
            "price": thiscart[0][2],
            "name": thiscart[0][0],
            "qty": thiscart[0][1],
            "idd": producto
            }

        list_dict.append(dict_prod)

    if request.method == "GET":
        conn.commit()
        conn.close()

        return render_template("cart.html", data=list_dict)

    conn.commit()
    conn.close()

    return render_template ("cart.html", data=list_dict)
@app.route("/delete", methods =["POST"])
def delete():
    idd = request.form.get("id")

    session["cart"].remove(idd)
    return redirect("/cart")

@app.route("/delivery", methods =["GET", "POST"])
def delivery():
    if request.method == "GET":
        pass

    if request.method == "POST":
        conn = sqlite3.connect('database.db')
        for producto in session["cart"]:
            c = conn.cursor()
            c.execute('''SELECT * FROM productos WHERE productID IN (?)''', (producto,))
            user_cart = c.fetchall()
            c.execute(('''INSERT INTRO transaction'''))
        conn.commit()
        conn.close()
        date = datetime.datetime.now()


if __name__ == '__main__':
    app.run()
