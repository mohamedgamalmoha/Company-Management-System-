# Generated by Django 3.2.8 on 2021-10-17 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_expiration_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('first_name', 'last_name')},
        ),
    ]
