# Generated by Django 4.1.3 on 2024-04-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0002_doctor_manager_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]