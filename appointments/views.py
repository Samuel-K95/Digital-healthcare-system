from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from .forms import AppointmentForm
from django.contrib import messages


@login_required
def ScheduleAppointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.appointment_date = form.cleaned_data['appointment_date']
            appointment.additional_requests = form.cleaned_data['additional_requests']
            appointment.save()
            messages.success(request, "Appointment Scheduled Successfully")
            return redirect('view_doctor_appointments')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = AppointmentForm()
    return render(request, 'doctors/schedule_appointment.html', {'form': form, 'doctor': doctor})


@login_required
def ViewMyPatientAppointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctors/patient_appointments.html', {'appointments': appointments, 'doctor': doctor})

@login_required
def ViewMyDoctorAppointments(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'patients/patient_appointments.html', {'appointments': appointments})

@login_required
def DeleteAppointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment Deleted Successfully")
    return redirect('view_doctor_appointments')

# @login_required
# def update_appointment_status(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id)
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         if status in ['accepted', 'declined', 'rescheduled']:
#             appointment.status = status
#             appointment.save()
#             return redirect('doctor_appointments', appointment.doctor.id)
#     return render(request, 'update_appointment_status.html', {'appointment': appointment})