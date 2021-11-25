from re import search
from typing import Tuple


def is_valid_choices(choices: list, values: list) -> bool:
    return all(val in choices for val in values)


def is_valid_choice(val) -> bool:
    return val and val is not None and not search(r'^-+$', val)


def start_end_date_prepare(year_start_date: int, month_start_date: int, year_end_date: int, month_end_date: int) \
        -> Tuple[int, int, int, int]:

    year_start_date, month_start_date = int(year_start_date), int(month_start_date)
    year_end_date, month_end_date = int(year_end_date), int(month_end_date)

    if year_end_date < year_start_date:
        year_end_date, year_start_date = year_start_date, year_end_date
        month_end_date, month_start_date = month_start_date, month_end_date

    if year_end_date == year_start_date and month_end_date < month_start_date:
        month_end_date, month_start_date = month_start_date, month_end_date

    return year_start_date, month_start_date, year_end_date, month_end_date
