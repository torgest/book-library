from db import get_conn

def search_books(title=None, author=None, genre=None, year_from=None, year_to=None):
    sql, params = "SELECT * FROM books WHERE 1=1", []
    if title:
        sql += " AND title  LIKE ?"; params.append(f"%{title}%")
    if author:
        sql += " AND author LIKE ?"; params.append(f"%{author}%")
    if genre:
        sql += " AND genre  = ?";    params.append(genre)
    if year_from is not None:
        sql += " AND year >= ?";     params.append(year_from)
    if year_to is not None:
        sql += " AND year <= ?";     params.append(year_to)
    sql += " ORDER BY author, title"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]