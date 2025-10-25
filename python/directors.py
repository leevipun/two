import db

def get_directors():
    sql = "SELECT id, name FROM directors"
    results = db.query(sql)
    return results if results else None

def get_movie_directors(movie_id):
    """Hae elokuvan kaikki ohjaajat"""
    sql = """SELECT d.id, d.name 
             FROM directors d
             JOIN movie_directors md ON d.id = md.director_id
             WHERE md.movie_id = ?"""
    results = db.query(sql, [movie_id])
    return results if results else []