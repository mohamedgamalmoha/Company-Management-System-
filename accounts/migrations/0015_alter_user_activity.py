# Generated by Django 3.2 on 2021-11-25 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affairs', '0010_alter_vacations_worker'),
        ('accounts', '0014_user_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affairs.activity'),
        ),
    ]
