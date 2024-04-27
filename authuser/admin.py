from django.contrib import admin
from .models import User
from .models import Doctor, Patient, Manager
# Register your models here.

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Manager)