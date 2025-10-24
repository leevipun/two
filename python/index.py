from flask import Flask, render_template, request, flash, redirect, session
import sqlite3
from werkzeug.security import check_password_hash
import os
import users
import db
from dotenv import load_dotenv
load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(current_dir), 'ui')
static_dir = os.path.join(os.path.dirname(current_dir), 'ui')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    
    if not result:
        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/login")
    
    password_hash = result[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    
    flash("VIRHE: väärä tunnus tai salasana")
    return redirect("/login")

@app.route('/logout')
def logout():
    del session["username"]
    return redirect("/")

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/create', methods=["POST"])
def create():
    username = request.form["username"]
    password = request.form["password"]
    password_conf = request.form["password_conf"]

    if password != password_conf:
        flash("Salasanat eivät täsmää")
        return redirect("/register")
    try:
        users.create_user(username, password)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")
        


if __name__ == '__main__':
    app.run(debug=True)