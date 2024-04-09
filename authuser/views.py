from django.shortcuts import render
from .models import Patient, Manager
from .forms import PatientForm
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required
# Create your views here
# .
@login_required(login_url='/login')
def profile(request):
    user = request.user
    ctx = {}
    ctx['user'] = user
    if user.is_patient:
        patient_instance = Patient.objects.get(user=user)
        ctx['form'] = PatientForm(instance=patient_instance)
        ctx['appointments'] = Appointment.objects.filter(patient=patient_instance)
        if request.method == 'POST':
            updated_form = PatientForm(request.POST, instance=patient_instance)
            if updated_form.is_valid():
                updated_form.save()
                return render(request, 'pages/profile.html', ctx)
    elif user.is_manager:
        # manager_instance = Manager.objects.get(user=user)
        # ctx['form'] = PatientForm(instance=patient_instance)
        ctx['appointments'] = Appointment.objects.all()
        
    return render(request, 'pages/profile.html', ctx)

