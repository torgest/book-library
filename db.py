import sqlite3
from contextlib import contextmanager

DB_PATH = "library.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    title    TEXT NOT NULL,
    author   TEXT NOT NULL,
    year     INTEGER NOT NULL CHECK (year BETWEEN 1 AND 2100),
    genre    TEXT NOT NULL,
    added_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_author ON books(author);
CREATE INDEX IF NOT EXISTS idx_genre  ON books(genre);
"""

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)

def add_book(title: str, author: str, year: int, genre: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)",
            (title.strip(), author.strip(), year, genre.strip()),
        )
        return cur.lastrowid

def get_all_books():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM books ORDER BY author, title"
        ).fetchall()]

def get_book(book_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        return dict(row) if row else None

def update_book(book_id: int, **fields) -> bool:
    allowed = {"title", "author", "year", "genre"}
    fields = {k: v for k, v in fields.items() if k in allowed}
    if not fields:
        return False
    cols = ", ".join(f"{k} = ?" for k in fields)
    with get_conn() as conn:
        cur = conn.execute(
            f"UPDATE books SET {cols} WHERE id = ?",
            (*fields.values(), book_id),
        )
        return cur.rowcount > 0

def delete_book(book_id: int) -> bool:
    with get_conn() as conn:
        return conn.execute(
            "DELETE FROM books WHERE id = ?", (book_id,)
        ).rowcount > 0