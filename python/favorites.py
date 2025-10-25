import db

def get_user_favorites(user_id):
    """Get all favorite movies for a user"""
    sql = """
    SELECT m.*, uf.created_at as favorited_at
    FROM movies m 
    JOIN user_favorites uf ON m.id = uf.movie_id 
    WHERE uf.user_id = ?
    ORDER BY uf.created_at DESC
    """
    results = db.query(sql, [user_id])
    return results if results else []

def toggle_favorite(user_id, movie_id):
    """Toggle favorite status for a movie"""
    # Check if already favorited
    check_sql = "SELECT id FROM user_favorites WHERE user_id = ? AND movie_id = ?"
    existing = db.query(check_sql, [user_id, movie_id])
    
    if existing:
        # Remove from favorites
        delete_sql = "DELETE FROM user_favorites WHERE user_id = ? AND movie_id = ?"
        db.execute(delete_sql, [user_id, movie_id])
        return False
    else:
        # Add to favorites
        insert_sql = "INSERT INTO user_favorites (user_id, movie_id) VALUES (?, ?)"
        db.execute(insert_sql, [user_id, movie_id])
        return True

def is_favorite(user_id, movie_id):
    """Check if a movie is favorited by user"""
    sql = "SELECT id FROM user_favorites WHERE user_id = ? AND movie_id = ?"
    result = db.query(sql, [user_id, movie_id])
    return len(result) > 0