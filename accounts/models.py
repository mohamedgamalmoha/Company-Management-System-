from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        unique_together = ['first_name', 'last_name']
        verbose_name = 'الادارة'
        verbose_name_plural = 'الادارة'

    def get_absolute_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.pk})


class Worker(models.Model):
    name = models.CharField('الاسم', max_length=150, unique=True)

    nationality = models.CharField('الجنسية', max_length=150)
    qid = models.CharField('QID', max_length=150)
    qid_expiration_date = models.DateField(' تاريخ انتهاء QID', null=True)
    passport_number = models.CharField('رقم الجواز', max_length=10, null=True)
    expiration_date = models.DateField(' تاريخ انتهاء الجواز', null=True)
    guarantee = models.CharField('الكفالة', max_length=150)
    settlement_id = models.CharField('اي دي الاقامة', max_length=150)

    basic_salary = models.DecimalField('الراتب الاساسي', max_digits=20, decimal_places=2, default=0.00)
    feeding_allowance = models.DecimalField('بدل غذاء', max_digits=20, decimal_places=2, default=0.00)
    housing_allowance = models.DecimalField('بدل سكن', max_digits=20, decimal_places=2, default=0.00)
    transporting_allowance = models.DecimalField('بدل انتقال', max_digits=20, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'العمال'
        verbose_name_plural = 'العمال'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('accounts:worker_detail', kwargs={'pk': self.pk})
