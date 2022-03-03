from datetime import datetime
from calendar import monthrange

from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.signals import post_save
from django.conf import settings
from django.shortcuts import reverse
from django.dispatch import receiver
from django.utils.formats import date_format
from django.utils import translation, timezone
from django.core.validators import ValidationError
from django.contrib.auth.backends import get_user_model

from accounts.models import Worker
from .managers import DayManager
from .decorators import debug, decimal_limit
from .utils import MONTHS_DICT, MONTHS_NAMES, YEARS_NUMBERS


User = get_user_model()


class Activity(models.Model):
    name = models.CharField('اسم النشاط', max_length=150)

    class Meta:
        verbose_name = 'النشاط'
        verbose_name_plural = 'النشاط'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('affairs:activity_detail', kwargs={'pk': self.pk})


class Location(models.Model):
    name = models.CharField('اسم الموقع', max_length=150)

    class Meta:
        verbose_name = 'الموقع'
        verbose_name_plural = 'الموقع'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('affairs:location_detail', kwargs={'pk': self.pk})


class Month(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='العميل', related_name='worker_months', null=True)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='اسم النشاط')
    month = models.CharField('الشهر', max_length=150, choices=MONTHS_NAMES, null=True)
    year = models.CharField('السنة', max_length=150, choices=YEARS_NUMBERS, null=True)

    class Meta:
        verbose_name = 'الشهر'
        verbose_name_plural = 'الشهر'
        unique_together = ('worker', 'month', 'year')

    def __str__(self):
        return f'{self.month} / {self.year} - {self.worker.name}' if self.worker else str(self.pk)

    def get_absolute_url(self):
        return reverse('affairs:month_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.year:
            self.year = timezone.now().year
        return super().save(*args, **kwargs)
    
    def all_days_location(self):
        locations_lst = []
        days = self.months.filter(location__isnull=False).distinct()
        for day in days:
            location_name = day.location.name
            if location_name and location_name not in locations_lst:
                locations_lst.append(location_name)
        return locations_lst

    def get_month_number(self):
        for month_num in MONTHS_DICT:
            if self.month in MONTHS_DICT[month_num]:
                return month_num
        return None

    def get_month_arabic(self):
        for tpl in MONTHS_DICT.values():
            if self.month in tpl:
                return tpl[1]
        return None

    def get_days_count(self):
        return monthrange(int(self.year), self.get_month_number())[1]

    def get_days_query(self):
        days = getattr(self, 'months', None)
        if days is None:
            raise ValidationError('There is no days for this month')
        return days.all()

    def get_activity(self):
        return self.activity or 'لا يوجد'

    @property
    def username(self):
        return self.worker.name if self.worker else 'لا يوجد'

    @property
    def date(self):
        return f"{self.month} / {self.year}"

    @property
    #@decimal_limit
    def hour_paid(self):
        return self.day_paid / 8

    @property
    #@decimal_limit
    def day_paid(self):
        return self.worker.basic_salary / 30

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
        return self.worker.feeding_allowance or 0
    feeding_allowance.short_description = 'بدل غذاء'

    def housing_allowance(self):
        return self.worker.housing_allowance or 0
    housing_allowance.short_description = 'بدل سكن'

    def transporting_allowance(self):
        return self.worker.transporting_allowance or 0
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
        return self.get_days_query().aggregate(Sum('deduction')).get('deduction__sum') or 0 #* self.hour_paid
    total_deduction.short_description = 'اجمالي الخصومات'

    def total_rewards(self):
        return self.get_days_query().aggregate(Sum('rewards')).get('rewards__sum') or 0
    total_rewards.short_description = 'اجمالي المكافئات'

    def total_loans(self):
        return self.get_days_query().aggregate(Sum('loans')).get('loans__sum') or 0
    total_loans.short_description = 'اجمالي السلف'

    def total_absence_hours(self):
        return 8 * self.absence_days_count
    total_absence_hours.short_description = 'عدد ساعات الغياب'

    @decimal_limit
    def total_absence_deduction(self):
        return self.get_total_absence_days() * self.day_paid
    total_absence_deduction.short_description = 'اجمالي خصم ساعات الغياب'

    def get_total_real_absence_days(self):
        return self.absence_days_count
    get_total_real_absence_days.short_description = 'اجمالي ايام الغياب الفعلية'

    def get_total_absence_days(self):
        return self.absence_days_count
    get_total_absence_days.short_description = 'اجمالي ايام الغياب'

    # Total section
    @decimal_limit
    def total_salary(self):
        return self.attendance_days_count * self.day_paid + self.get_total_allowance() + self.total_extra_work_hours_money() + self.total_rewards()
    total_salary.short_description = 'اجمالي المرتب'

    # @decimal_limit
    def total_salary_deduction(self):
        return self.total_deduction() + self.total_loans() + self.total_absence_deduction()
    total_salary_deduction.short_description = 'اجمالي الخصم'

    @decimal_limit
    def net_salary(self):
        absence_deduction = self.get_total_absence_days() * self.day_paid
        total_deduction = absence_deduction + self.total_loans() + self.total_deduction()
        extra_hours_fees = self.total_extra_work_hours() * self.hour_paid
        attendance_fees = self.attendance_days_count * self.day_paid
        total_extra = self.total_rewards() + extra_hours_fees + attendance_fees + self.get_total_allowance()
        return total_extra - total_deduction
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

    objects = DayManager()

    class Meta:
        verbose_name = 'اليوم'
        verbose_name_plural = 'اليوم'

    def __str__(self):
        return f'{self.day_number}'

    def get_absolute_url(self):
        return reverse('affairs:day_detail', kwargs={'pk': self.pk})

    def get_attendance_arabic(self):
        return 'Y' if self.attendance else 'N'

    def get_location_arabic(self):
        return self.location or 'لا يوجد'

    @debug(prefix='In affairs model ')
    def get_day_name(self):
        date_time_str = f"{self.day_number}/{self.month.month}/{self.month.year}"
        date_time_obj = datetime.strptime(date_time_str, '%d/%b/%Y')
        translation.activate(settings.LANGUAGE_CODE)
        return date_format(date_time_obj, 'l')

    def is_friday(self):
        return self.get_day_name() == 'الجمعة'


class Vacations(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='الموظف', related_name='vacations', null=True)
    reason = models.TextField('السبب')
    start_date = models.DateField('بداية من')
    end_date = models.DateField('نهاية الي')

    class Meta:
        verbose_name = 'الاجازات'
        verbose_name_plural = 'الاجازات'

    def __str__(self):
        return f'  اجازة {self.username}  '

    def get_absolute_url(self):
        return reverse('affairs:vacations_detail', kwargs={'pk': self.pk})

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
        for day in range(1, days + 1):
            Day.objects.create(month=instance, day_number=day)
