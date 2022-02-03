from decimal import Decimal, ROUND_UP

from django.db.models import Manager, Sum, Count, Case, When, Value


def update_day(dct: dict) -> dict:
    hour_paid = Decimal(dct.get('month__worker__basic_salary', 0)) / Decimal(30 * 8)
    total_extra_hours_paid = dct.get('total_extra_hours') * hour_paid
    total_deduction_paid = Decimal(dct.get('total_loans', 0)) + Decimal(dct.get('total_deduction', 0)) + Decimal(dct.get('num_of_absence', 0)) * hour_paid * 8
    total_paid = Decimal(dct.get('num_of_attendance') * 8 * hour_paid + total_extra_hours_paid - total_deduction_paid).quantize(Decimal('.01'), rounding=ROUND_UP)
    dct.update({
        'hour_paid': hour_paid,
        'total_extra_hours_paid': total_extra_hours_paid,
        'total_deduction_paid': total_deduction_paid,
        'total_paid': total_paid
    })
    return dct


class DayManager(Manager):
    def group_by_location(self) -> list:
        return list(map(update_day, self.values('location__id', 'location__name', 'month__id', 'month__worker__basic_salary').annotate(
            total_extra_hours=Sum('extra_work_hours'),
            total_deduction=Sum('deduction'),
            total_rewards=Sum('rewards'),
            total_loans=Sum('loans'),
            num_of_attendance=Count(Case(When(attendance=True, then=Value(1)))),
            num_of_absence=Count(Case(When(attendance=False, then=Value(1)))),
        ).order_by('location__id')))

    def group_by_location_given_id(self, locations) -> list:
        query = self.group_by_location()
        length = len(locations) - len(query)
        if length > 0:
            query.extend([None for _ in range(length)])
        sorted_list1 = [x for _, x in sorted(zip(locations, query), key=lambda pair: pair[0].get('id'))]
        return sorted_list1
