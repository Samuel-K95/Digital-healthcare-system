from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('schedule_appointment/<int:doctor_id>/', views.ScheduleAppointment, name='schedule_appointment'),
    path('view_doctor_appointments/', views.ViewMyDoctorAppointments, name='view_doctor_appointments'),
    path('view_patient_appointments/', views.ViewMyPatientAppointments, name='view_patient_appointments'),
    path('delete_appointment/<int:appointment_id>/', views.DeleteAppointment, name='delete_appointment'),
    path('edit_appointment/<int:appointment_id>/', views.EditAppointment, name='edit_appointment'),
    path('confirm_appointment/<int:appointment_id>/', views.ConfirmAppointment, name='confirm_appointment'),
    path('reschedule_appointment/<int:appointment_id>/', views.RescheduleAppointment, name='reschedule_appointment'),
    # path('reschedule_appointment/<int:appointment_id>/', views.RescheduleAppointment, name='reschedule_appointment'),
    # path('confirm_appointment/<int:doctor_id>/', views.ConfirmAppointment, name='confirm_appointment'),
    # path('cancel_appointment/<int:appointment_id>/', views.CancelAppointment, name='cancel_appointment'),
]