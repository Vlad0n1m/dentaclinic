from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from authuser.models import Patient, Manager, Doctor, User
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment
from datetime import datetime
from django.core.serializers import serialize
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
    return render(request, "pages/index.html")


from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm


@login_required(login_url="/login")
def create_appointment(request):

    user = request.user
    ctx = {}
    ctx["user"] = user
    if not user.is_patient:
        return render(
            request,
            "appointments/create_appointment.html",
            {"error": "Эта страница предназначена для записи на прием для пациентов"},
        )
    if request.method == "POST":
        # Make a mutable copy of request.POST
        post_copy = request.POST.copy()
        doctor_id = post_copy.pop("doctorId", None)[0]

        form = AppointmentForm(post_copy)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = (
                "R"  # Устанавливаем статус по умолчанию как "Запрошено"
            )
            appointment.patient = Patient.objects.get(user=user)
            appointment.doctor = Doctor.objects.get(pk=doctor_id)
            appointment.save()
            return JsonResponse(
                {"status": "success", "message": appointment.pk}, status=200
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Форма не валидна"}, status=405
            )
    else:
        form = AppointmentForm()
    doctors = User.objects.filter(is_doctor=1).values("id", "username")
    return render(
        request,
        "appointments/create_appointment.html",
        {"form": form, "doctors": doctors},
    )


# def get_free_dates(req):
@login_required(login_url="/login")
def available_slots(request):
    date_str = request.GET.get("date")
    doctor_id = request.GET.get("doctor")
    if date_str and doctor_id:
        selected_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        selected_datetime = datetime.combine(selected_date, datetime.min.time())
        aware_selected_datetime = timezone.make_aware(
            selected_datetime
        )  # Создание осведомлённого datetime
        doctor = Doctor.objects.get(pk=doctor_id)
    else:
        return JsonResponse([], safe=False)

    start_of_day = aware_selected_datetime.replace(
        hour=9, minute=0, second=0, microsecond=0
    )
    slots = [start_of_day + timedelta(hours=i) for i in range(9)]  # Генерация 9 слотов

    doctor_data = {
        "achiewmens": doctor.achievements,
        "education": doctor.education,
        "email": doctor.user.email,
        "username": doctor.user.username
    }
    
    busy_slots = Appointment.objects.filter(
        doctor=doctor,
        time__range=(start_of_day, start_of_day + timedelta(days=1)),
        status__in=["R", "A"],  # Запрошено, Подтверждено
    )
    busy_times = [slot.time for slot in busy_slots]
    free_slots = [slot for slot in slots if slot not in busy_times]
    print(busy_times)
    print(free_slots)
    ctx = {'free_slots': free_slots, 'doctor': doctor_data }

    return JsonResponse(ctx, safe=False)


def appointment_detail(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    return render(
        request, "appointments/appointment_detail.html", {"appointment": appointment}
    )


def manager_actions(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    # Добавьте вашу логику здесь для принятия, отклонения или изменения времени записи
    return render(
        request, "appointments/manager_actions.html", {"appointment": appointment}
    )


def manager_actions(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    user = appointment.patient.user
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "accept":
            # Set appointment status to 'A' (Accepted)
            appointment.status = "A"
            appointment.save()
            return redirect("appointment_detail", pk=pk)

        elif action == "reject":
            # Set appointment status to 'C' (Cancelled)
            appointment.status = "C"
            appointment.save()
            return redirect("appointment_detail", pk=pk)

        elif action == "modify":
            form = AppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                form.save()
                return redirect("appointment_detail", pk=pk)

    else:
        form = AppointmentForm(instance=appointment)

    return render(
        request,
        "appointments/manager_actions.html",
        {"appointment": appointment, "form": form, "user": user},
    )
