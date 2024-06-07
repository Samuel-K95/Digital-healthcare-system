from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from . import gemini
from .forms import PatientForm, UserForm, UserLoginForm, GeminiChatForm
from django.urls import reverse


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
    return render(request, 'patients/patient_profile.html', {'patient': curr_patient})


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
            chat = gemini.Chat()
            request.session['chat'] = chat.serialize()
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
                chat = gemini.Chat()
                request.session['chat'] = chat.serialize()
                return redirect('PatientDashboard', pk=user.pk)
    else:
        user_form  = UserLoginForm()
    
    return render(request, 'patients/patient_login.html', {'user_form':user_form})
                

def GeminiChat(request):
    if request.method == 'POST':
        chat_form = GeminiChatForm(request.POST)
        if chat_form.is_valid():
            chat_data = request.session.get('chat')
            if chat_data:
                chat = gemini.Chat.deserialize(chat_data)
                if len(chat.messages) == 0:
                    rep = chat.gemini_new_request(chat_form.cleaned_data.get('question'))
                else:
                    rep = chat.gemini_request(chat_form.cleaned_data.get('question'))

                request.session['chat'] = chat.serialize()
            return JsonResponse({'response' :rep})
    else:
        chat_form = GeminiChatForm()
    
    return render(request, 'patients/base.html', {'chat_form': chat_form})

def Posts(request):
    pass

def PatientAppointments(request):
    pass

def Doctors(request):
    pass

def Messages(request):
    pass

def PatientLogout(request):
    logout(request)
    next_page = request.GET.get('next', 'PatientLogin')
    return redirect(reverse(next_page))
    