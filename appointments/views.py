from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from .forms import AppointmentForm, RescheduleAppointmentForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



def ScheduleAppointment(request, doctor_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to login before scheduling an appointment!")
        return redirect('PatientLogin')
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
    return render(request, 'patients/schedule_appointment.html', {'form': form, 'doctor': doctor})


@login_required
def ViewMyPatientAppointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctors/patient_appointments.html', {'appointments': appointments, 'doctor': doctor})

@login_required
def ViewMyDoctorAppointments(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'patients/doctor_appointments.html', {'appointments': appointments})

@login_required
def DeleteAppointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment Deleted Successfully")
    return redirect('view_doctor_appointments')



@login_required
def RescheduleAppointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = RescheduleAppointmentForm(request.POST)
        if form.is_valid():
            appointment.appointment_date = form.cleaned_data['appointment_date']
            appointment.save()
            messages.success(request, "Appointment Rescheduled Successfully!")
            return redirect('view_patient_appointments')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RescheduleAppointmentForm()
    
    return render(request, 'doctors/reschedule_appointment.html', {'form': form})

@login_required
def EditAppointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment.appointment_date = form.cleaned_data['appointment_date']
            appointment.additional_requests = form.cleaned_data['additional_requests']
            appointment.save()
            messages.success(request, "Appointment Edited Successfully!")
            return redirect('view_doctor_appointments')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = AppointmentForm()
    
    return render(request, 'patients/edit_appointment.html', {'form': form})


@login_required
def StartVideoCall(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    room_id = str(appointment.id) 
    if(Doctor.objects.filter(user=request.user).exists()):
        doc = Doctor.objects.get(user=request.user)
        full_name = f"Dr. {doc.first_name} {doc.last_name}"    
    else:
        full_name = f"{request.user}"    

    return render(request, 'communication/video_call.html', {'full_name': full_name, 'room_id':room_id})
    
@login_required
def JoinTheCall(request, appointment_id):
    roomID = str(appointment_id)
    meeting_link = f'http://localhost:8000/Appointments/VideoCall/{roomID}/?roomID={roomID}'
    return redirect(meeting_link)

    

@login_required
def ConfirmAppointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.status = 'accepted'

    # Generate the video call link
    doc = Doctor.objects.get(user=request.user)
    full_name = f"Dr. {doc.first_name} {doc.last_name}"
    room_id = str(appointment.id)  # Use the appointment ID as the room ID
    # video_call_link = f"{request.scheme}://{request.get_host()}/video_call/?roomID={room_id}"
    # video_call_link = f"http://localhost:8000/Appointments/VideoCall/13/?roomID=3832"
    video_call_link = f"http://localhost:8000/Appointments/VideoCall/14/?roomID={room_id}"
    appointment.video_call_link = video_call_link

    appointment.save()


    # Send an email to the patient with the video call link
    patient_email = appointment.patient.user.email
    subject = "Video Call Link for Your Appointment"
    message = f"Dear {appointment.patient.user.first_name},\n\n"
    message += f"{full_name} has confirmed your appointment.\n"
    message += f"Please click the following link to join the video call:\n"
    message += f"{video_call_link}\n\n"
    message += "Best regards,\n"
    message += "MediConnect Team"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient_email],
        fail_silently=False,
    )

    messages.success(request, "Appointment Accepted Successfully")
    return redirect('view_patient_appointments')