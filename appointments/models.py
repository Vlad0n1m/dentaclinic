from django.db import models
from django.dispatch import receiver
from authuser.models import Patient, Doctor

class Appointment(models.Model):
    STATUSES = {
        ('R', 'Запрошено'),
        ('A', 'Подтверждено'),
        ('S', 'Состоялось'),
        ('C', 'Отменено')
    }
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, verbose_name="Врач", on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    time = models.DateTimeField(verbose_name="Время")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUSES, verbose_name="Статус")
    date_created = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now_add=True, verbose_name="Дата обновления")