from werkzeug.security import check_password_hash, generate_password_hash

import db 

def get_movies():
    sql = """
    SELECT m.*,
           c.name as genre,
           sp.name as platform,
           d.name as director
    FROM movies m
    LEFT JOIN categories c ON m.category_id = c.id
    LEFT JOIN streaming_platforms sp ON m.streaming_platform_id = sp.id
    LEFT JOIN directors d ON m.director_id = d.id
    ORDER BY m.created_at DESC
    """
    results = db.query(sql)
    
    # Convert to list of dictionaries for easier handling
    movies = []
    for row in results:
        movie_dict = dict(row)
        movies.append(movie_dict)
        
    return movies if movies else []

def get_movie_by_id(movie_id, user_id=None):
    """Get a single movie by ID with favorite status if user_id provided"""
    import favorites  # Import here to avoid circular import
    
    sql = """
        SELECT 
            m.*,
            c.name AS genre,
            d.name AS director,
            s.name AS platform
        FROM movies m
        LEFT JOIN categories c ON m.category_id = c.id
        LEFT JOIN streaming_platforms s ON m.streaming_platform_id = s.id
        LEFT JOIN directors d ON m.director_id = d.id
        WHERE m.id = ?
    """
    results = db.query(sql, [movie_id])
    
    if not results:
        return None
    
    movie = dict(results[0])
    
    # Add favorite status if user is logged in
    if user_id:
        movie['is_favorite'] = favorites.is_favorite(user_id, movie_id)
    else:
        movie['is_favorite'] = False
    
    return movie

def get_or_add_director(director_name):
    """Get director by name or create new one"""
    if not director_name or director_name.strip() == '':
        return None
    
    # Check if director exists
    sql = "SELECT id FROM directors WHERE name = ?"
    result = db.query(sql, [director_name.strip()])
    
    if result:
        return result[0]['id']
    
    # Add new director
    insert_sql = "INSERT INTO directors (name) VALUES (?)"
    db.execute(insert_sql, [director_name.strip()])
    return db.last_insert_id()

def add_movie(user_id, movie):
    if not user_id:
        return "User ID is required."
    
    # Handle director
    director_id = None
    if movie.get("director") and movie["director"].strip():
        director_id = get_or_add_director(movie["director"])
    
    # Insert movie into the movies table
    sql = """INSERT INTO movies 
                (title, 
                year, 
                duration, 
                category_id,
                streaming_platform_id,
                director_id,
                watch_date, 
                rating, 
                watched_with,
                review, 
                favorite, 
                rewatchable, 
                user_id) 
            VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    params = (
        movie["title"],
        movie["year"] if movie["year"] else None,
        movie["duration"] if movie["duration"] else None,
        movie.get("genre") if movie.get("genre") else None,
        movie.get("platform") if movie.get("platform") else None,
        director_id,
        movie["watch_date"] if movie["watch_date"] else None,
        movie["rating"] if movie["rating"] else None,
        movie["watched_with"] if movie["watched_with"] else None,
        movie["review"] if movie["review"] else None,
        bool(movie.get("favorite", False)),
        bool(movie.get("rewatchable", False)),
        user_id
    ) 
    
    db.execute(sql, params)
    return db.last_insert_id()