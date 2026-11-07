import db
import validation as v
from search import search_books
from stats import summary, stats_by_genre, stats_by_author
from reports import export_txt, export_html

def show_books(books):
    if not books:
        print("— Список пуст —")
        return
    print(f"{'ID':>4} | {'Автор':<20} | {'Название':<30} | {'Год':>4} | Жанр")
    print("-" * 90)
    for b in books:
        print(f"{b['id']:>4} | {b['author'][:20]:<20} | "
              f"{b['title'][:30]:<30} | {b['year']:>4} | {b['genre']}")

def cmd_add():
    try:
        title  = v.require_non_empty(input("Название: "), "Название")
        author = v.require_non_empty(input("Автор: "), "Автор")
        year   = v.validate_year(input("Год: "))
        genre  = v.require_non_empty(input("Жанр: "), "Жанр")
    except ValueError as e:
        print(f"⚠ {e}")
        return
    book_id = db.add_book(title, author, year, genre)
    print(f"✓ Добавлено, id = {book_id}")

def cmd_list():
    show_books(db.get_all_books())

def cmd_search():
    print("Оставьте поле пустым, чтобы не фильтровать по нему.")
    title  = input("Название содержит: ").strip() or None
    author = input("Автор содержит: ").strip() or None
    genre  = input("Жанр (точно): ").strip() or None
    yf_raw = input("Год от: ").strip()
    yt_raw = input("Год до: ").strip()
    yf = int(yf_raw) if yf_raw.isdigit() else None
    yt = int(yt_raw) if yt_raw.isdigit() else None
    show_books(search_books(title, author, genre, yf, yt))

def cmd_edit():
    try:
        book_id = int(input("ID книги: "))
    except ValueError:
        print("⚠ ID должен быть числом")
        return
    book = db.get_book(book_id)
    if not book:
        print("⚠ Книга не найдена")
        return
    print(f"Текущее: {book}")
    print("Введите новое значение или Enter, чтобы оставить.")
    updates = {}
    for field, label in [("title", "Название"), ("author", "Автор"),
                         ("year", "Год"), ("genre", "Жанр")]:
        val = input(f"{label}: ").strip()
        if not val:
            continue
        try:
            if field == "year":
                val = v.validate_year(val)
            else:
                val = v.require_non_empty(val, label)
        except ValueError as e:
            print(f"⚠ {e}")
            return
        updates[field] = val
    if db.update_book(book_id, **updates):
        print("✓ Обновлено")
    else:
        print("⚠ Нечего обновлять")

def cmd_delete():
    try:
        book_id = int(input("ID книги для удаления: "))
    except ValueError:
        print("⚠ ID должен быть числом")
        return
    book = db.get_book(book_id)
    if not book:
        print("⚠ Книга не найдена")
        return
    print(f"Удалить: {book['author']} — {book['title']}?")
    if input("Подтвердите (y/n): ").lower() != "y":
        print("Отменено")
        return
    db.delete_book(book_id)
    print("✓ Удалено")

def cmd_stats():
    s = summary()
    print(f"\nВсего книг: {s['total']}, авторов: {s['authors']}, "
          f"жанров: {s['genres']}, годы: {s['oldest']}–{s['newest']}\n")
    print("По жанрам:")
    for r in stats_by_genre():
        print(f"  {r['genre']}: {r['cnt']}")
    print("\nПо авторам:")
    for r in stats_by_author():
        print(f"  {r['author']}: {r['cnt']}")

def cmd_export():
    kind = input("Формат (txt/html): ").strip().lower()
    if kind == "txt":
        print("Сохранено:", export_txt())
    elif kind == "html":
        print("Сохранено:", export_html())
    else:
        print("⚠ Неизвестный формат")

def menu():
    db.init_db()
    while True:
        print("""
=== Домашняя библиотека ===
1. Добавить книгу
2. Показать все книги
3. Поиск
4. Редактировать книгу
5. Удалить книгу
6. Статистика
7. Экспорт отчёта (TXT/HTML)
0. Выход
""")
        choice = input("Выбор: ").strip()
        if   choice == "1": cmd_add()
        elif choice == "2": cmd_list()
        elif choice == "3": cmd_search()
        elif choice == "4": cmd_edit()
        elif choice == "5": cmd_delete()
        elif choice == "6": cmd_stats()
        elif choice == "7": cmd_export()
        elif choice == "0": print("До свидания!"); break
        else: print("⚠ Нет такого пункта")

if __name__ == "__main__":
    menu()