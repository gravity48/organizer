from typing import List, Tuple


DAYS_IN_YEAR = 365
DAYS_IN_MONTH = 30


def plural_russian_date(
    *,
    year: int = 0,
    month: int = 0,
    days: int = 0,
) -> str:
    """Склоняет дату по падежам."""
    fields = [
        (year, ['лет', 'год', 'года']),
        (month, ['месяцев', 'месяц', 'месяца']),
        (days, ['дней', 'день', 'дня']),
    ]
    format_dates = []
    for field in fields:
        if not field[0]:
            continue
        format_dates.append(f'{field[0]} {plural_word_by_value(field[0], field[1])}')
    return ' '.join(format_dates)


def plural_word_by_value(value: int, words: List[str]) -> str:
    """Склоняет существительное по падежам."""
    remainder = value % 10
    if value == 0 or remainder == 0 or remainder >= 5 or value in range(11, 19):
        return words[0]
    elif remainder == 1:
        return words[1]
    else:
        return words[2]


def days_to_ymd(days: int) -> Tuple:
    """Конвертирует дни в года/месяца/дни."""
    years = days // DAYS_IN_YEAR
    remaining_days = days % DAYS_IN_YEAR
    months = remaining_days // DAYS_IN_MONTH
    remaining_days = remaining_days % DAYS_IN_MONTH
    return years, months, remaining_days
