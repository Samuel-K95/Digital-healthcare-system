from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="PatientHome"),
    path('PatientDashboard/<int:pk>', views.PatientDashboard, name="PatientDashboard"),
    path('PatientProfile/<int:pk>', views.PatientProfile, name="PatientProfile"),
    path('PatientSignUp/', views.PatientSignUp, name="PatientSignUp"),
    path('PatientLogin/', views.PatientLogin, name="PatientLogin"),
    path('Posts/<int:pk>', views.Posts, name="Posts"),
    path('PatientAppointments/<int:pk>', views.PatientAppointments, name="PatientAppointments"),
    path('Doctors/<int:pk>', views.Doctors, name="Doctors"),
    path('Messages/<int:pk>', views.Messages, name="Messages"),
    path('PatientLogout/', views.PatientLogout, name="PatientLogout"),
    path('PatientGeminiChat/', views.chat_app, name="PatientGeminiChat"),
]

