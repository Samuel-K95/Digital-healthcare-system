from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name="dashboard"),
    path('DoctorProfile/', views.DoctorProfile, name="DoctorProfile"),
    path('DoctorSignUp/', views.registerDoctor, name="DoctorSignUp"),
    path('DoctorLogin/', views.DoctorLogin, name="DoctorLogin"),
    path('DoctorLogout/', views.DoctorLogout, name="DoctorLogout"),
    path('BrowseDoctors/', views.BrowseDoctors, name="BrowseDoctors"),
    path('DoctorDetail/<int:pk>', views.DoctorDetail, name="DoctorDetail"),

]