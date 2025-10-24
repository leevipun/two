import db

def add_favorite(user_id, movie_id):
    """Add a movie to user's favorites"""
    sql = "INSERT OR IGNORE INTO user_favorites (user_id, movie_id) VALUES (?, ?)"
    return db.execute(sql, [user_id, movie_id])

def remove_favorite(user_id, movie_id):
    """Remove a movie from user's favorites"""
    sql = "DELETE FROM user_favorites WHERE user_id = ? AND movie_id = ?"
    return db.execute(sql, [user_id, movie_id])

def is_favorite(user_id, movie_id):
    """Check if a movie is in user's favorites"""
    sql = "SELECT 1 FROM user_favorites WHERE user_id = ? AND movie_id = ?"
    result = db.query(sql, [user_id, movie_id])
    return bool(result)

def get_user_favorites(user_id):
    """Get all favorite movies for a user"""
    sql = """
    SELECT m.*, uf.created_at as favorited_at 
    FROM movies m 
    JOIN user_favorites uf ON m.id = uf.movie_id 
    WHERE uf.user_id = ? 
    ORDER BY uf.created_at DESC
    """
    return db.query(sql, [user_id])

def toggle_favorite(user_id, movie_id):
    """Toggle favorite status - add if not favorite, remove if already favorite"""
    if is_favorite(user_id, movie_id):
        remove_favorite(user_id, movie_id)
        return False
    else:
        add_favorite(user_id, movie_id)
        return True