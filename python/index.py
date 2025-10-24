from flask import Flask, render_template, request, flash, redirect, session, jsonify, get_flashed_messages
import sqlite3
from werkzeug.security import check_password_hash
import os
import users
import movies
import db
import favorites
from dotenv import load_dotenv
load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(current_dir), 'ui')
static_dir = os.path.join(os.path.dirname(current_dir), 'ui')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def index():
    if "username" in session:
        user = users.get_user(session["username"])
        if user:
            user_movies = movies.get_movies()
            print(user_movies)
            return render_template('index.html', movies=user_movies)
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Clear any existing flash messages to ensure fresh start
        get_flashed_messages()
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
    # Clear any existing flash messages to ensure fresh start
    get_flashed_messages()
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
    session["username"] = username
    return redirect("/")
        
@app.route('/add', methods=["POST", "GET"])
def add():
    if "username" not in session:
        return redirect("/login")
    user = users.get_user(session["username"])
    if not user:
        return redirect("/login")
    if request.method == "GET":
        return render_template("add.html")
    
    # Handle POST request to add movie
    movie_data = {
        "title": request.form.get("title"),
        "year": request.form.get("year") or None,
        "duration": request.form.get("duration") or None,
        "director": request.form.get("director") or None,
        "genre": request.form.get("genre") or None,
        "watch_date": request.form.get("watchDate") or None,
        "rating": request.form.get("rating") or None,
        "watched_with": request.form.get("watchedWith") or None,
        "platform": request.form.get("platform") or None,
        "review": request.form.get("review") or None,
        "favorite": bool(request.form.get("favorite")),
        "rewatchable": bool(request.form.get("rewatchable"))
    }
    
    movies.add_movie(user["id"], movie_data)
    flash("Movie added successfully!", "success")
    return redirect("/")

@app.route('/favorites')
def user_favorites():
    if "username" not in session:
        return redirect("/login")
    
    user = users.get_user(session["username"])
    if not user:
        return redirect("/login")
    
    user_favorites_list = favorites.get_user_favorites(user["id"])
    return render_template('favorites.html', favorites=user_favorites_list)

@app.route('/toggle_favorite/<int:movie_id>', methods=["POST"])
def toggle_favorite_route(movie_id):
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    user = users.get_user(session["username"])
    if not user:
        return jsonify({"error": "User not found"}), 401
    
    is_now_favorite = favorites.toggle_favorite(user["id"], movie_id)
    return jsonify({"is_favorite": is_now_favorite})

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    user_id = None
    if "username" in session:
        user = users.get_user(session["username"])
        user_id = user["id"] if user else None
    
    movie = movies.get_movie_by_id(movie_id, user_id)
    if not movie:
        flash("Movie not found")
        return redirect("/")
    
    return render_template('movie_detail.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)