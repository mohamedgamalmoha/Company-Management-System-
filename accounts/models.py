from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nationality = models.CharField('الجنسية', max_length=150)
    basic_salary = models.DecimalField('الراتب الاساسي', max_digits=20, decimal_places=2, default=0.00)
    feeding_allowance = models.DecimalField('بدل غذاء',  max_digits=20, decimal_places=2, default=0.00)
    housing_allowance = models.DecimalField('بدل سكن',  max_digits=20, decimal_places=2, default=0.00)
    transporting_allowance = models.DecimalField('بدل انتقال',  max_digits=20, decimal_places=2, default=0.00)
    passport_number = models.CharField('رقم الجواز', max_length=10, null=True)
    expiration_date = models.DateField(' تاريخ انتهاء الجواز', null=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        unique_together = ['first_name', 'last_name']
        verbose_name = 'المستخدمين'
        verbose_name_plural = 'المستخدمين'
