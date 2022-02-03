from django import template


register = template.Library()


@register.filter(name='group_days_by_locations')
def group_by_locations(months, locations):
    if hasattr(months, 'group_by_location_given_id'):
        return getattr(months, 'group_by_location_given_id')(locations)
