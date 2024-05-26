from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="PatientHome"),
    path('PatientProfile/', views.PatientProfile, name="PatientProfile"),
    path('PatientSignUp/', views.PatientSignUp, name="PatientSignUp")
]