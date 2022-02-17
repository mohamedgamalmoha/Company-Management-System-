from django import template


ARABIC_NUMBERS = {
    '0': '٠',
    '1': '١',
    '2': '٢',
    '3': '٣',
    '4': '٤',
    '5': '٥',
    '6': '٦',
    '7': '٧',
    '8': '٨',
    '9': '٩	'
}

register = template.Library()


@register.filter(name='group_days_by_locations')
def group_by_locations(months, locations) -> list:
    if hasattr(months, 'group_by_location_given_id'):
        return getattr(months, 'group_by_location_given_id')(locations)


@register.filter(name='sum_locations')
def sum_locations(locations: list) -> float:
    return sum(location.get('total_paid') for location in locations if location)


@register.filter
def total_paid_location(months, locations) -> list:

    result = map(lambda month: getattr(month.months, 'group_by_location_given_id')(locations), months)
    flatten_result = [j for sub in result for j in sub if j]
    dict_result = {}
    for i in flatten_result:
        _id = i.get('location__id')
        dict_result[_id] = dict_result.get(_id, 0) + i.get('total_paid')
    sorted_result = sorted(dict_result.items(), key=lambda i: i[0])

    ids = [i for i, _ in sorted_result]
    values = [o for _, o in sorted_result]
    locations_ids = list(map(lambda i: i.get('id'), locations))

    indexes = map(lambda item: locations_ids.index(item), set(locations_ids) - set(ids))
    for iter_index, index in enumerate(indexes):
        values.insert(index + iter_index, None)
    return values


@register.filter
def translate_number(number: str) -> str:
    return "".join([ARABIC_NUMBERS.get(char, '-') for char in number if char in ARABIC_NUMBERS])
