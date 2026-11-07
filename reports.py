from datetime import datetime
from html import escape
from db import get_all_books

def export_txt(path="report.txt"):
    books = get_all_books()
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Отчёт по библиотеке — {datetime.now():%d.%m.%Y %H:%M}\n")
        f.write("=" * 60 + "\n")
        for b in books:
            f.write(f"[{b['id']}] {b['author']} — «{b['title']}» "
                    f"({b['year']}), {b['genre']}\n")
        f.write("=" * 60 + f"\nВсего книг: {len(books)}\n")
    return path

HTML_TEMPLATE = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<title>Библиотека — отчёт</title>
<style>
body{{font-family:Arial,sans-serif;margin:2em}}
table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ccc;padding:6px;text-align:left}}
th{{background:#eee}}
</style></head><body>
<h1>Отчёт по домашней библиотеке</h1>
<p>Сформирован: {now}</p>
<table>
<tr><th>#</th><th>Автор</th><th>Название</th><th>Год</th><th>Жанр</th></tr>
{rows}
</table>
<p><b>Всего книг:</b> {total}</p>
</body></html>"""

def export_html(path="report.html"):
    books = get_all_books()
    rows = "\n".join(
        f"<tr><td>{b['id']}</td><td>{escape(b['author'])}</td>"
        f"<td>{escape(b['title'])}</td><td>{b['year']}</td>"
        f"<td>{escape(b['genre'])}</td></tr>"
        for b in books
    )
    html = HTML_TEMPLATE.format(
        now=f"{datetime.now():%d.%m.%Y %H:%M}",
        rows=rows,
        total=len(books),
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path