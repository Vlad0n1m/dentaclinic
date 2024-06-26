# Generated by Django 3.2.1 on 2024-04-16 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0009_alter_appointment_comment_alter_appointment_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('S', 'Состоялось'), ('C', 'Отменено'), ('R', 'Запрошено'), ('A', 'Подтверждено')], max_length=1, verbose_name='Статус'),
        ),
    ]
