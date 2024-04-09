# Generated by Django 4.1.3 on 2024-04-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('C', 'Отменено'), ('A', 'Подтверждено'), ('R', 'Запрошено'), ('S', 'Состоялось')], max_length=1, verbose_name='Статус'),
        ),
    ]