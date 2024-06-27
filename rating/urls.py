from django.urls import path
from . import views



urlpatterns = [
    path('rate_doctor/<int:doctor_id>/', views.RateDoctor, name = 'rate_doctor'),        
]