# Generated by Django 3.2.1 on 2024-04-26 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0008_alter_user_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='achievements',
            field=models.TextField(blank=True, null=True, verbose_name='Достижения'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='education',
            field=models.TextField(blank=True, null=True, verbose_name='Образование'),
        ),
    ]
