# Generated by Django 3.2.1 on 2024-04-16 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0004_alter_doctor_date_updated_alter_patient_date_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Номер телефона'),
        ),
    ]
