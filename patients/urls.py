from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="PatientHome"),
    path('PatientHome/', views.PatientProfile, name="PatientProfile")
]