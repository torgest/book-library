from db import get_conn

def summary():
    with get_conn() as conn:
        row = conn.execute("""
            SELECT COUNT(*)               AS total,
                   COUNT(DISTINCT author) AS authors,
                   COUNT(DISTINCT genre)  AS genres,
                   MIN(year)              AS oldest,
                   MAX(year)              AS newest
            FROM books
        """).fetchone()
        return dict(row)

def stats_by_genre():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT genre, COUNT(*) AS cnt FROM books GROUP BY genre ORDER BY cnt DESC"
        )]

def stats_by_author():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT author, COUNT(*) AS cnt FROM books GROUP BY author ORDER BY cnt DESC"
        )]