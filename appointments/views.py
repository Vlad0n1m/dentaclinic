from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from authuser.models import Patient, Manager, Doctor
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=request.user)
#     return render(request, 'profile.html', {'form': form})

def index(request):
    return render(request, 'pages/index.html')


from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
@login_required(login_url='/login')
def create_appointment(request):
    
    user = request.user
    ctx = {}
    ctx['user'] = user
    if not user.is_patient:
        return render(request, 'appointments/create_appointment.html', {'error': 'ur not a patient'})
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'R'  # Устанавливаем статус по умолчанию как "Запрошено"
            appointment.patient = Patient.objects.get(user=user)
            appointment.save()
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})

def appointment_detail(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

def manager_actions(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    # Добавьте вашу логику здесь для принятия, отклонения или изменения времени записи
    return render(request, 'appointments/manager_actions.html', {'appointment': appointment})




def manager_actions(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    user = appointment.patient.user
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
            # Set appointment status to 'A' (Accepted)
            appointment.status = 'A'
            appointment.save()
            return redirect('appointment_detail', pk=pk)
        
        elif action == 'reject':
            # Set appointment status to 'C' (Cancelled)
            appointment.status = 'C'
            appointment.save()
            return redirect('appointment_detail', pk=pk)
        
        elif action == 'modify':
            form = AppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                form.save()
                return redirect('appointment_detail', pk=pk)
    
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/manager_actions.html', {'appointment': appointment, 'form': form, 'user':user})
