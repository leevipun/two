from werkzeug.security import check_password_hash, generate_password_hash

import db 
import users

def get_movies():
    sql = "SELECT id, title, genre, rating, year, review FROM movies"
    results = db.query(sql)
    return results if results else None

def add_movie(user_id, movie):
    sql = """INSERT INTO movies 
                (title, 
                year, 
                duration, 
                director, 
                watch_date, 
                rating, 
                watched_with, 
                platform, 
                review, 
                favorite, 
                rewatchable, 
                user_id) 
            VALUES 
                (?, 
                ?, 
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?, 
                ?)"""
    params = (movie["title"],
              movie["year"],
              movie["duration"],
              movie["director"],
              movie["watch_date"],
              movie["rating"],
              movie["watched_with"],
              movie["platform"],
              movie["review"],
              bool(movie["favorite"]),
              bool(movie["rewatchable"]),
              user_id) 
    db.execute(sql, params)