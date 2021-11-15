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

    rng = range(index, 13) if greater else range(index+1)

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


def get_range_months_by_indexes(max_index: int, min_index: int):

    if not str(max_index).isnumeric() or not str(min_index).isnumeric():
        raise ValueError('parameters must be numeric')

    if max_index > 12 or min_index > 12:
        raise ValueError('numbers must be less tgan 12')

    if max_index < min_index:
        max_index, min_index = min_index, max_index

    return (MONTHS_DICT[index][index] for index in range(min_index, max_index))


def get_range_months_lte_index(index: int):
    if not str(index).isnumeric():
        raise ValueError('index must be numeric')
    if index > 12:
        raise ValueError('numbers must be less than 12')
    return (MONTHS_DICT.get(ind)[0] for ind in range(1, index+1))


def get_range_months_gte_index(index: int):
    if not str(index).isnumeric():
        raise ValueError('index must be numeric')
    if index > 12:
        raise ValueError('numbers must be less tgan 12')
    return (MONTHS_DICT.get(ind)[0] for ind in range(index, len(MONTHS_DICT) + 1))


MONTHS_NAMES = MONTHS_DICT.values()
MONTHS_NAMES_ENG = (month[0] for month in MONTHS_DICT.values())
MONTHS_NUMBERS = MONTHS_DICT.keys()
YEARS_NUMBERS = tuple((str(year), str(year)) for year in years_range())
