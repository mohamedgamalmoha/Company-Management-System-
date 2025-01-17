# Generated by Django 3.2.8 on 2021-10-23 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_worker_name'),
        ('affairs', '0007_alter_vacations_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacations',
            name='user',
        ),
        migrations.AddField(
            model_name='month',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_months', to='accounts.worker', verbose_name='العميل'),
        ),
        migrations.AddField(
            model_name='vacations',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacations', to='accounts.worker', verbose_name='العميل'),
        ),
        migrations.AlterUniqueTogether(
            name='month',
            unique_together={('worker', 'month', 'year')},
        ),
        migrations.RemoveField(
            model_name='month',
            name='user',
        ),
    ]
