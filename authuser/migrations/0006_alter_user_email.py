# Generated by Django 3.2.1 on 2024-04-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0005_patient_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
