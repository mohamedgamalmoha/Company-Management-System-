# Generated by Django 3.2.8 on 2022-02-03 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affairs', '0010_alter_vacations_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='month',
            field=models.CharField(choices=[('Jan', 'يناير'), ('Feb', 'فبراير'), ('Mar', 'مارس'), ('Apr', 'أبريل'), ('May', 'مايو'), ('Jun', 'يونيو'), ('Jul', 'يوليو'), ('Aug', 'أغسطس'), ('Sep', 'سبتمبر'), ('Oct', 'أكتوبر'), ('Nov', 'نوفمبر'), ('Dec', 'ديسمبر')], max_length=150, null=True, verbose_name='الشهر'),
        ),
        migrations.AlterField(
            model_name='month',
            name='year',
            field=models.CharField(choices=[('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027')], max_length=150, null=True, verbose_name='السنة'),
        ),
    ]