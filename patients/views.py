from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import *
from .forms import PatientForm, UserForm, UserLoginForm

# Create your views here.

def index(request):
    return HttpResponse("index home")

def PatientDashboard(request, pk):
    patient = get_object_or_404(Patient, user__pk=pk)
    context = {
        'patient' : patient
    }
    
    return render(request, 'patients/dashboard.html', context)

def PatientProfile(request, pk):
    curr_patient=get_object_or_404(Patient, user__pk=pk)
    return render(request, 'patients/patient_profile.html', {'patients': curr_patient.__str__()})


def PatientSignUp(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST)

        if patient_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.email = user_form.cleaned_data.get('email')
            patient.password = user_form.cleaned_data.get('password1')
            patient.save()

            patient_form = PatientForm(request.POST, instance=user.patient)
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username = user.username, password = raw_password)
            login(request, user)
            return redirect('PatientDashboard', pk = user.pk) 
    else:
        patient_form = PatientForm()
        user_form = UserForm()
    return render(request, 'patients/PatientSignUp.html', {'user_form':user_form, 'patient_form': patient_form})


def PatientLogin(request):
    if request.method == 'POST':
        user_form  = UserLoginForm(request.POST)

        if user_form.is_valid():
            user = user_form.get_user()
            if user is not None:
                login(request, user)
                return redirect('PatientDashboard', pk=user.pk)
    else:
        user_form  = UserLoginForm()
    
    return render(request, 'patients/patient_login.html', {'user_form':user_form})
                


def Posts(request):
    pass

def PatientAppointments(request):
    pass

def Doctors(request):
    pass

def Messages(request):
    pass

def PatientLogout(request):
    pass