# Generated by Django 3.2.8 on 2021-11-15 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20211023_2157'),
        ('affairs', '0009_alter_month_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacations',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacations', to='accounts.worker', verbose_name='الموظف'),
        ),
    ]
