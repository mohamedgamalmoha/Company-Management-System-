from calendar import monthrange

from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from django.core.validators import ValidationError
from django.contrib.auth.backends import get_user_model

from accounts.models import Worker
from .decorators import decimal_limit
from .utils import MONTHS_DICT, MONTHS_NAMES, YEARS_NUMBERS


User = get_user_model()


class Activity(models.Model):
    name = models.CharField('اسم النشاط', max_length=150)

    class Meta:
        verbose_name = 'النشاط'
        verbose_name_plural = 'النشاط'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField('اسم الموقع', max_length=150)

    class Meta:
        verbose_name = 'الموقع'
        verbose_name_plural = 'الموقع'

    def __str__(self):
        return self.name


class Month(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='العميل', related_name='worker_months', null=True)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='اسم النشاط')
    month = models.CharField('الشهر', max_length=150, choices=MONTHS_NAMES)
    year = models.CharField('السنة', max_length=150, choices=YEARS_NUMBERS)

    class Meta:
        verbose_name = 'الشهر'
        verbose_name_plural = 'الشهر'
        unique_together = ('worker', 'month', 'year')

    def __str__(self):
        return f'{self.month} / {self.year} - {self.worker.name}' if self.worker else self.pk

    def save(self, *args, **kwargs):
        if not self.year:
            self.year = timezone.now().year
        return super().save(*args, **kwargs)

    def get_month_number(self):
        for month_num in MONTHS_DICT:
            if self.month in MONTHS_DICT[month_num]:
                return month_num
        return None

    def get_days_count(self):
        return monthrange(int(self.year), self.get_month_number())[1]

    def get_days_query(self):
        days = getattr(self, 'months', None)
        if days is None:
            raise ValidationError('There is no days for this month')
        return days.all()

    @property
    def username(self):
        return self.worker.name if self.worker else 'لا يوجد'

    @property
    def date(self):
        return f"{self.month} / {self.year}"

    @property
    @decimal_limit
    def hour_paid(self):
        return self.worker.basic_salary / (30 * 8)

    @property
    def absence_days(self):
        return self.get_days_query().filter(attendance=False)

    @property
    def absence_days_count(self):
        return self.absence_days.count()

    @property
    def attendance_days_count(self):
        return self.get_days_query().count() - self.absence_days.count()

    # Basic User Section
    def basic_salary(self):
        return self.worker.basic_salary
    basic_salary.short_description = 'الراتب الاساسي'

    def feeding_allowance(self):
        return self.worker.feeding_allowance
    feeding_allowance.short_description = 'بدل غذاء'

    def housing_allowance(self):
        return self.worker.housing_allowance
    housing_allowance.short_description = 'بدل سكن'

    def transporting_allowance(self):
        return self.worker.transporting_allowance
    transporting_allowance.short_description = 'بدل انتقال'

    def get_total_allowance(self):
        return self.feeding_allowance() + self.housing_allowance() + self.transporting_allowance()
    get_total_allowance.short_description = 'اجمالي البدالات'

    # Basic Month Section
    def total_extra_work_hours(self):
        return self.get_days_query().aggregate(Sum('extra_work_hours')).get('extra_work_hours__sum') or 0
    total_extra_work_hours.short_description = 'اجمالي عدد الساعات الاضافية'

    @decimal_limit
    def total_extra_work_hours_money(self):
        return self.total_extra_work_hours() * self.hour_paid
    total_extra_work_hours_money.short_description = 'اجمالي قيمة الساعات الاضافية'

    def total_deduction(self):
        return self.get_days_query().aggregate(Sum('deduction')).get('deduction__sum') or 0
    total_deduction.short_description = 'اجمالي الخصومات'

    def total_rewards(self):
        return self.get_days_query().aggregate(Sum('rewards')).get('rewards__sum') or 0
    total_rewards.short_description = 'اجمالي المكافئات'

    def total_loans(self):
        return self.get_days_query().aggregate(Sum('loans')).get('loans__sum') or 0
    total_loans.short_description = 'اجمالي السلف'

    def total_absence_hours(self):
        return 2 * 8 * self.absence_days_count
    total_absence_hours.short_description = 'عدد ساعات الغياب'

    @decimal_limit
    def total_absence_deduction(self):
        return self.total_absence_hours() * self.hour_paid
    total_absence_deduction.short_description = 'اجمالي خصم ساعات الغياب'

    def get_total_real_absence_days(self):
        return self.absence_days_count
    get_total_real_absence_days.short_description = 'اجمالي ايام الغياب الفعلية'

    def get_total_absence_days(self):
        return self.absence_days_count * 2
    get_total_absence_days.short_description = 'اجمالي ايام الغياب'

    # Total section
    @decimal_limit
    def total_salary(self):
        return self.basic_salary() + self.get_total_allowance() + self.total_extra_work_hours_money() + self.total_rewards()
    total_salary.short_description = 'اجمالي المرتب'

    @decimal_limit
    def total_salary_deduction(self):
        return self.total_deduction() + self.total_loans() + self.total_absence_deduction()
    total_salary_deduction.short_description = 'اجمالي الخصم'

    @decimal_limit
    def net_salary(self):
        return self.total_salary() - self.total_salary_deduction()
    net_salary.short_description = 'صاقي المرتب'


class Day(models.Model):
    month = models.ForeignKey(Month, on_delete=models.SET_NULL, null=True, verbose_name='الشهر', related_name='months')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name='الموقع', blank=True)
    day_number = models.IntegerField('رقم اليوم', )
    attendance = models.BooleanField('الحضور', default=True)
    extra_work_hours = models.DecimalField('عدد سعات عمل اضافية', default=0.0,  max_digits=20, decimal_places=2)
    deduction = models.DecimalField('الخصم', default=0.0,  max_digits=20, decimal_places=2)
    rewards = models.DecimalField('المكافئات', default=0.0,  max_digits=20, decimal_places=2)
    loans = models.DecimalField('السلف', default=0.0,  max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = 'اليوم'
        verbose_name_plural = 'اليوم'

    def __str__(self):
        return f'{self.day_number}'


class Vacations(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='العميل', related_name='vacations', null=True)
    reason = models.TextField('السبب')
    start_date = models.DateField('بداية من')
    end_date = models.DateField('نهاية الي')

    class Meta:
        verbose_name = 'الاجازات'
        verbose_name_plural = 'الاجازات'

    @property
    def username(self):
        return self.worker.name if self.worker else 'لا يوجد'

    @property
    def duration(self):
        return self.end_date - self.start_date

    @property
    def duration_in_days(self):
        return self.duration.days

    def clean(self):
        if not self.start_date:
            raise ValidationError('هذا الحقل مطلوب')
        if not self.end_date:
            raise ValidationError('هذا الحقل مطلوب')
        if self.start_date > self.end_date:
            raise ValidationError('لا يمكن البداية ان تكون اكبر من النهاية')


@receiver(post_save, sender=Month)
def create_days_for_month(sender, instance, created, **kwargs):
    if created:
        days = instance.get_days_count()
        for day in range(days):
            Day.objects.create(month=instance, day_number=day)
