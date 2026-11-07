import pytest
import db
from search import search_books

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()

def test_add_and_search():
    db.add_book("Мастер и Маргарита", "Булгаков", 1967, "роман")
    result = search_books(author="Булгаков")
    assert len(result) == 1
    assert result[0]["title"] == "Мастер и Маргарита"

def test_update():
    book_id = db.add_book("Книга", "Автор", 2000, "жанр")
    assert db.update_book(book_id, year=2001) is True
    assert db.get_book(book_id)["year"] == 2001

def test_delete():
    book_id = db.add_book("1984", "Оруэлл", 1949, "антиутопия")
    assert db.delete_book(book_id) is True
    assert db.delete_book(book_id) is False

def test_validation_year():
    import validation as v
    assert v.validate_year("1967") == 1967
    with pytest.raises(ValueError):
        v.validate_year("3000")
    with pytest.raises(ValueError):
        v.validate_year("abc")