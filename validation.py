from datetime import date

def require_non_empty(value: str, field: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"Поле «{field}» не может быть пустым")
    return value

def validate_year(value) -> int:
    try:
        year = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError("Год должен быть целым числом")
    current = date.today().year
    if not (1 <= year <= current + 1):
        raise ValueError(f"Год должен быть в диапазоне 1..{current + 1}")
    return year