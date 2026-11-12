"""Функции очистки данных выгрузки."""


def normalize_city(city: str | None) -> str | None:
    """Убирает пробелы по краям и делает первую букву заглавной."""
    if city is None:
        return None
    return city.strip().title()

def parse_amount(value: str | None) -> int | None:
    """Превращает сумму из выгрузки в int; если не получилось — None."""
    try:
        return int(value.replace(' ', ''))
    except (ValueError, AttributeError):
        return None