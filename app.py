from flask import Flask, render_template, request, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
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
    if len(session) > 0:
        user = session["user_id"]
        return render_template("home.html", category=category_data, user=user)
    if "user_id" not in session:
        return render_template("home.html", category=category_data)


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
            conn.commit()
            conn.close()
        except NameError:
            return"existe"
        session["user_id"] = username
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
        session["user_id"] = user[0][1]
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
    list_dict =[]
    for producto in session["cart"]:
        c = conn.cursor()
        c.execute('''SELECT * FROM productos WHERE productID IN (?)''', (producto,))
        user_cart = c.fetchall()
        dict_prod = {
                      "price": user_cart[0][2],
                       "name": user_cart[0][1]
                     }
        list_dict.append(dict_prod)
    conn.commit()
    conn.close()
    return render_template ("cart.html", data = list_dict)
##cart html, admin route + htlm

if __name__ == '__main__':
    app.run()
