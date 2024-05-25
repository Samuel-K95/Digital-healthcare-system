from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def index(request):
    return HttpResponse("index home")

def PatientProfile(request):
    all_users = Patient.objects.all()
    return render(request, 'patients/patient_profile.html', {'patients':all_users.__str__()})
    