from typing import List

from django.utils import timezone


MONTHS_DICT = {
    1: ("Jan", "يناير"),
    2: ("Feb", "فبراير"),
    3: ("Mar", "مارس"),
    4: ("Apr", "أبريل"),
    5: ("May", "مايو"),
    6: ("Jun", "يونيو"),
    7: ("Jul", "يوليو"),
    8: ("Aug", "أغسطس"),
    9: ("Sep", "سبتمبر"),
    10: ("Oct", "أكتوبر"),
    11: ("Nov", "نوفمبر"),
    12: ("Dec", "ديسمبر"),
}


def years_range(num_range=5) -> List[int]:
    now_time = timezone.now()
    return list(range((now_time.year - num_range), (now_time.year + num_range + 1)))


def get_list_months(month, greater=True):
    index = None

    for key, val in MONTHS_DICT.items():
        if month in val:
            index = key
            break

    if index is None:
        raise ValueError('The passed month doesnt match')

    rng = range(index, 13) if greater else range(0, index+1)

    return [(MONTHS_DICT.get(i)[0], MONTHS_DICT.get(i)[0]) for i in rng]


def get_range_months(start, end):
    start_index = None
    end_index = None

    for key, val in MONTHS_DICT.items():
        if start in val:
            start_index = key
        if end in val:
            end_index = key
            break

    if start_index is None or end_index is None:
        raise ValueError('invalid value')

    return [(MONTHS_DICT.get(i)[0], MONTHS_DICT.get(i)[0]) for i in range(start_index, end_index)]


MONTHS_NAMES = MONTHS_DICT.values()
MONTHS_NUMBERS = MONTHS_DICT.keys()
YEARS_NUMBERS = ((year, year) for year in years_range())
