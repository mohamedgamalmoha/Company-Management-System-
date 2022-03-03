from decimal import Decimal, ROUND_UP

from django.db.models import Manager, Sum, Count, Case, When, Value, F


def update_day(dct: dict) -> dict:
    # a) num of days in each location                      (Done)
    # b) all days in month: attendance=True                (Done)
    # c) basic salary                                      (Done)
    # d) day paid = c / 30 & hour paid = d1 / 8            (Done)
    # e) extra hours * d2 & rewords                        (Done)
    # f) deduction & loans                                 (Done)
    # g) num of absence days month: attendance=False       (Done)
    # h) absence_deduction = d1 * g                        (Done)
    # i) total location paid = d1 * a + e - f - h
    # total salary = d1 * a + e - f

    num_of_absence_days = dct.get('num_of_absence', 0)                                          # g
    days_count = dct.get('days_count', 0)                                                       # a
    num_of_attendance_days = dct.get('num_of_attendance', 0)                                    # b
    day_paid = dct.get('month__worker__basic_salary', 0) / 30                                   # d1
    hour_paid = day_paid / 8                                                                    # d2
    extra_hours_paid = dct.get('total_extra_hours', 0) * hour_paid                              # e1
    total_deduction_and_loan_paid = dct.get('total_loans', 0) + dct.get('total_deduction', 0)   # f
    total_extra_hours_and_rewords_paid = extra_hours_paid + dct.get('total_rewards', 0)         # e
    absence_deduction = day_paid * num_of_absence_days                                          # h
    attendance_paid = day_paid * num_of_attendance_days
    total_paid = attendance_paid - absence_deduction + total_extra_hours_and_rewords_paid - total_deduction_and_loan_paid
    dct.update({
        'total_paid': total_paid.quantize(Decimal('.01'), rounding=ROUND_UP)
    })
    return dct


class DayManager(Manager):

    def group_by_location(self) -> list:
        dct = self.values('location__id',  'month__worker__name', 'month__month', 'month__year',  'month__worker__basic_salary').annotate(
            total_extra_hours=Sum('extra_work_hours'),
            total_deduction=Sum('deduction'),
            total_rewards=Sum('rewards'),
            total_loans=Sum('loans'),
            days_count=Count('location__id'),
            num_of_attendance=Count(Case(When(attendance=True, location__id=F('location__id'), then=Value(1)))),
            num_of_absence=Count(Case(When(attendance=False, location__id=F('location__id'), then=Value(1)))),
        ).exclude(location__id__isnull=True).order_by('location__id')
        return list(map(update_day, dct))

    def group_by_location_given_id(self, locations) -> list:
        query = self.group_by_location()
        locations_ids = list(map(lambda i: i.get('id'), locations))
        query_ids = set(map(lambda i: i.get('location__id'), query))
        indexes = map(lambda i: locations_ids.index(i), set(locations_ids) - query_ids)
        for iter_index, index in enumerate(indexes):
            query.insert(index + iter_index, {})
        return query
