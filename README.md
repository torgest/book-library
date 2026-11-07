# Домашняя библиотека (Кейс 10)

Консольное приложение на Python для учёта книг. Данные хранятся в SQLite.

## Запуск
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py

## Тесты

## Возможности
- CRUD книг (автор, название, год, жанр)
- поиск по названию/автору/жанру/годам
- статистика по жанрам и авторам
- отчёты TXT и HTML

## Структура
- main.py — меню
- db.py — работа с базой
- search.py — поиск
- stats.py — статистика
- reports.py — отчёты
- validation.py — проверка ввода
- tests/ — тесты

