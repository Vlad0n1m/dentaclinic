from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['time', 'comment']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
            
        }