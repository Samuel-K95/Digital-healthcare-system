from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from . import gemini
from .forms import PatientForm, UserForm, UserLoginForm, GeminiChatForm, PatientProfileForm, MedicalHistoryForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("index home")

def PatientDashboard(request, pk):
    patient = get_object_or_404(Patient, user__pk=pk)
    context = {
        'patient' : patient 
    }
    
    return render(request, 'patients/dashboard.html', context)

def PatientProfile(request):
    curr_patient=get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=curr_patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('PatientProfile')
    else:
        form = PatientProfileForm(instance=curr_patient)

    return render(request, 'patients/patient_profile.html', {'form': form,'pat': curr_patient})


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
                return redirect('PatientProfile')
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


def view_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_histories = patient.medical_histories.all()
    return render(request, 'Medical_History/medical_history.html', {'patient': patient, 'medical_histories': medical_histories})


@login_required
def add_diagnostic_results(request, patient_id):
    doctor = Doctor.objects.get(user=request.user)
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient = patient
            medical_history.doctor = doctor
            medical_history.save()
            return redirect('view_medical_history', patient_id=patient.id)
    else:
        form = MedicalHistoryForm()
    return render(request, 'Medical_History/add_diagnostic_results.html', {'form': form, 'patient': patient})









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
    

