from flask import Flask, render_template, request, flash, redirect, session, jsonify, get_flashed_messages
import sqlite3
from werkzeug.security import check_password_hash
import os
import users
import movies
import categories
import platforms
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
    user_movies = []
    if "username" in session:
        user = users.get_user(session["username"])
        if user:
            user_movies = movies.get_movies()
    return render_template('index.html', movies=user_movies)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        get_flashed_messages()
        return render_template('login.html')
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Please enter both username and password")
        return redirect("/login")

    user = users.get_user(username)
    
    if not user:
        flash("Invalid username or password")
        return redirect("/login")

    if check_password_hash(user['password_hash'], password):
        session["username"] = username
        return redirect("/")
    
    flash("Invalid username or password")
    return redirect("/login")

@app.route('/logout')
def logout():
    if "username" in session:
        del session["username"]
    return redirect("/")

@app.route('/register')
def register():
    get_flashed_messages()
    return render_template('register.html')

@app.route('/create', methods=["POST"])
def create():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    password_conf = request.form.get("password_conf", "")

    if not username or not password:
        flash("Username and password are required")
        return redirect("/register")

    if password != password_conf:
        flash("Passwords do not match")
        return redirect("/register")
    
    try:
        users.create_user(username, password)
        session["username"] = username
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("Username already exists")
        return redirect("/register")
        
@app.route('/add', methods=["POST", "GET"])
def add():
    if "username" not in session:
        return redirect("/login")
    
    user = users.get_user(session["username"])
    if not user:
        return redirect("/login")
        
    if request.method == "GET":
        category_list = categories.get_categories()
        platform_list = platforms.get_platforms()
        return render_template("add.html", categories=category_list, platforms=platform_list)
    
    # Handle POST request to add movie
    movie_data = {
        "title": request.form.get("title", "").strip(),
        "year": request.form.get("year") or None,
        "duration": request.form.get("duration") or None,
        "director": request.form.get("director", "").strip() or None,
        "genre": request.form.get("genre") or None,
        "watch_date": request.form.get("watchDate") or None,
        "rating": request.form.get("rating") or None,
        "watched_with": request.form.get("watchedWith", "").strip() or None,
        "platform": request.form.get("platform") or None,
        "review": request.form.get("review", "").strip() or None,
        "favorite": bool(request.form.get("favorite")),
        "rewatchable": bool(request.form.get("rewatchable"))
    }
    
    if not movie_data["title"]:
        flash("Movie title is required", "error")
        category_list = categories.get_categories()
        platform_list = platforms.get_platforms()
        return render_template("add.html", categories=category_list, platforms=platform_list)
    
    try:
        movies.add_movie(user["id"], movie_data)
        flash("Movie added successfully!", "success")
    except Exception as e:
        flash(f"Error adding movie: {str(e)}", "error")
    
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

@app.route('/search')
def search():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)