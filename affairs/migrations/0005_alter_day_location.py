# Generated by Django 3.2.8 on 2021-10-15 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affairs', '0004_alter_month_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affairs.location', verbose_name='الموقع'),
        ),
    ]
