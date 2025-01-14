# Generated by Django 3.2.8 on 2021-10-14 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='basic_salary',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='الراتب الاساسي'),
        ),
        migrations.AlterField(
            model_name='user',
            name='feeding_allowance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='بدل غذاء'),
        ),
        migrations.AlterField(
            model_name='user',
            name='housing_allowance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='بدل سكن'),
        ),
        migrations.AlterField(
            model_name='user',
            name='transporting_allowance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='بدل انتقال'),
        ),
    ]
