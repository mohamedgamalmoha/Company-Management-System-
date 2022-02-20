from decimal import Decimal, ROUND_UP

from django.db.models import Manager, Sum, Count, Case, When, Value


def update_day(dct: dict) -> dict:
    num_of_days = dct.get('num_of_attendance') + dct.get('num_of_absence')
    # basic_salary + total_allowance + extra_work_hours_money + total_rewards
    hour_paid = Decimal(dct.get('month__worker__basic_salary', 0)) / Decimal(30 * 8)  # hour paid
    total_extra_paid = dct.get('total_extra_hours') * hour_paid + dct.get('total_rewards')  # extra hours + rewords
    total_deduction_paid = Decimal(dct.get('total_loans', 0)) + Decimal(dct.get('total_deduction', 0)) + \
                           Decimal(dct.get('num_of_absence', 0)) * hour_paid * 8  # loan + deduction + absence
    total_paid = Decimal(dct.get('month__worker__basic_salary') + total_extra_paid - total_deduction_paid) \
        .quantize(Decimal('.01'), rounding=ROUND_UP)  # basic salary + extra - deduction
    dct.update({
        'hour_paid': hour_paid,
        'total_extra_hours_paid': total_extra_paid,
        'total_deduction_paid': total_deduction_paid,
        'total_paid': total_paid
    })
    return dct


class DayManager(Manager):

    def group_by_location(self) -> list:
        return list(map(update_day, self.values('location__id', 'location__name', 'month__id',
                                                'month__worker__basic_salary').annotate(
            total_extra_hours=Sum('extra_work_hours'),
            total_deduction=Sum('deduction'),
            total_rewards=Sum('rewards'),
            total_loans=Sum('loans'),
            num_of_attendance=Count(Case(When(attendance=True, then=Value(1)))),
            num_of_absence=Count(Case(When(attendance=False, then=Value(1)))),
        ).exclude(location__id__isnull=True).order_by('location__id')))

    def group_by_location_given_id(self, locations) -> list:
        query = self.group_by_location()
        locations_ids = list(map(lambda i: i.get('id'), locations))
        query_ids = set(map(lambda i: i.get('location__id'), query))
        indexes = map(lambda i: locations_ids.index(i), set(locations_ids) - query_ids)
        for iter_index, index in enumerate(indexes):
            query.insert(index + iter_index, {})
        return query
