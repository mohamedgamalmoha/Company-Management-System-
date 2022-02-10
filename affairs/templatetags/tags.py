from django import template


register = template.Library()


@register.filter(name='group_days_by_locations')
def group_by_locations(months, locations):
    if hasattr(months, 'group_by_location_given_id'):
        return getattr(months, 'group_by_location_given_id')(locations)


@register.filter(name='sum_locations')
def sum_locations(locations: list):
    return sum(location.get('total_paid') for location in locations if location)
