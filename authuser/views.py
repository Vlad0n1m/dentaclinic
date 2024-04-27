from django.shortcuts import render
from .models import Patient, Manager
from .forms import PatientForm, DoctorForm
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponseNotFound
from .models import User, Doctor
from django.views.decorators.http import require_http_methods


# Create your views here
# .
@login_required(login_url="/login")
def replace_status(request):
    if request.method == "POST":
        # Получаем id события из тела запроса
        event_id = request.POST.get("eventId")
        status = request.POST.get("status")

        try:
            # Находим запись в модели Appointment по id
            appointment = Appointment.objects.get(pk=event_id)

            # Изменяем статус на ваш выбранный
            appointment.status = status
            appointment.save()

            # Возвращаем JSON-ответ с успешным сообщением
            return JsonResponse(
                {"status": "success", "message": "Статус успешно изменен"}
            )
        except Appointment.DoesNotExist:
            # Если запись не найдена, возвращаем JSON-ответ с сообщением об ошибке
            return JsonResponse(
                {"status": "error", "message": "Запись не найдена"}, status=404
            )
    else:
        # Если запрос не является POST-запросом, возвращаем ошибку "Метод не разрешен"
        return JsonResponse(
            {"status": "error", "message": "Метод не разрешен"}, status=405
        )


@require_http_methods(["POST"])
def update_event(request, event_id):
    # Здесь должен быть код для обработки данных формы
    try:
        event = Appointment.objects.get(id=event_id)

        doctor_id = request.POST.get("doctor_id")
        patient_id = request.POST.get("patient_id")
        status = request.POST.get("status")
        time = request.POST.get("time")
        # Обновление данных в базе данных, например
        # Здесь вы должны добавить вашу логику обновления модели события
        if doctor_id and isinstance(doctor_id, int):
            event.doctor_id = doctor_id
        if patient_id and isinstance(patient_id, int):
            event.patient_id = patient_id
        if status:
            event.status = status
        if time:
            event.time = time.replace("T", " ") + ":00"

        # Сохраняем обновленное событие
        event.save()

        return JsonResponse(
            {"status": "success", "message": "Event updated successfully!"}
        )
    except Appointment.DoesNotExist:
        return HttpResponseNotFound({"status": "error", "message": "Event not found."})


@require_http_methods(["DELETE"])
def delete_event(request, event_id):
    try:
        event = Appointment.objects.get(pk=event_id)
        event.delete()
        return JsonResponse(
            {
                "status": "success",
                "message": f"Event with id {event_id} has been deleted.",
            }
        )
    except Appointment.DoesNotExist:
        return HttpResponseNotFound({"status": "error", "message": "Event not found."})


@login_required(login_url="/login")
def add_event(request):
    if request.method == "POST":
        # Получаем id события из тела запроса
        event_id = request.POST.get("eventId")
        status = request.POST.get("status")

        try:
            # Находим запись в модели Appointment по id
            appointment = Appointment.objects.get(pk=event_id)

            # Изменяем статус на ваш выбранный
            appointment.status = status
            appointment.save()

            # Возвращаем JSON-ответ с успешным сообщением
            return JsonResponse(
                {"status": "success", "message": "Статус успешно изменен"}
            )
        except Appointment.DoesNotExist:
            # Если запись не найдена, возвращаем JSON-ответ с сообщением об ошибке
            return JsonResponse(
                {"status": "error", "message": "Запись не найдена"}, status=404
            )
    else:
        # Если запрос не является POST-запросом, возвращаем ошибку "Метод не разрешен"
        return JsonResponse(
            {"status": "error", "message": "Метод не разрешен"}, status=405
        )


@login_required(login_url="/login")
def profile(request):
    user = request.user
    ctx = {}
    ctx["user"] = user
    if user.is_patient:
        patient_instance = Patient.objects.get(user=user)
        apointment_exists = Appointment.objects.filter(patient=patient_instance)
        ctx["form"] = PatientForm(instance=patient_instance)
        ctx["appointments"] = (
            Appointment.objects.filter(patient=patient_instance)
            if apointment_exists
            else []
        )
        if request.method == "POST":
            updated_form = PatientForm(request.POST, instance=patient_instance)
            if updated_form.is_valid():
                updated_form.save()
                return JsonResponse(
                    {"status": "success", "message": "Профиль  успешно изменен"}
                )
            else:
                return JsonResponse(
                    {"status": "error", "message": "Не удалось создать профиль"}, status=404
                )
    elif user.is_manager:
        appointments = Appointment.objects.all()
        data = []
        

        for ap in appointments:
            doctor = User.objects.filter(id=ap.doctor_id).first()
            doctor_data = doctor.username if doctor else "не назначен"

            patient = User.objects.filter(id=ap.patient_id).first()
            patient_data = patient.username if patient else "не назначен"

            data.append(
                {
                    "id": ap.id,
                    "title": doctor_data,  # Или другое поле, которое вы хотите использовать в качестве заголовка
                    "start": localtime(ap.time).isoformat() if ap.time else None,
                    "end": (
                        (localtime(ap.time) + timedelta(hours=1)).isoformat()
                        if ap.time
                        else None
                    ),  # Пример добавления 1 часа к начальному времени
                    "comment": ap.comment,
                    "patient": patient_data,  # Подобным образом добавьте данные пациента
                    "status": ap.status,
                }
            )
        ctx = {"appointments": data}

    elif user.is_doctor:
        appointments = Appointment.objects.filter(doctor=user.id)
        data = []

        doctorinstance = Doctor.objects.get(pk=user.id)
        form = DoctorForm(instance=doctorinstance)  
                
        for ap in appointments:
            doctor = User.objects.filter(id=ap.doctor_id).first()
            doctor_data = doctor.username if doctor else "не назначен"

            patient = User.objects.filter(id=ap.patient_id).first()
            patient_data = patient.username if patient else "не назначен"

            data.append(
                {
                    "id": ap.id,
                    "title": doctor_data,  # Или другое поле, которое вы хотите использовать в качестве заголовка
                    "start": localtime(ap.time).isoformat() if ap.time else None,
                    "end": (
                        (localtime(ap.time) + timedelta(hours=1)).isoformat()
                        if ap.time
                        else None
                    ),  # Пример добавления 1 часа к начальному времени
                    "comment": ap.comment,
                    "patient": patient_data,  # Подобным образом добавьте данные пациента
                    "status": ap.status,
                }
            )
        ctx = {"appointments": data, 'form': form}
        
        if request.method == "POST":
            updated_form = DoctorForm(request.POST, instance=doctorinstance)
            if updated_form.is_valid():
                updated_form.save()
            render(request, "pages/profile.html", ctx)

    return render(request, "pages/profile.html", ctx)
