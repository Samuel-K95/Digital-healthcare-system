from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import Doctor
from .forms import DoctorsProfileForm, UserLoginForm, UserForm
from django.urls import reverse
from django.contrib import messages



def index(request):
    return HttpResponse("index home")

def DoctorDashboard(request, pk):
    doctor = get_object_or_404(Doctor, user__pk=pk)
    context = {
        'doctor' : doctor  
    }
    
    return render(request, 'doctors/dashboard.html', context)

def DoctorProfile(request, pk):
    curr_doctor = get_object_or_404(Doctor, user__pk=pk)
    return render(request, 'doctors/doctors_profile.html', {'doctor': curr_doctor})

def registerDoctor(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        # doc_form = DoctorsProfileForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            # doc = doc_form.save(commit=False)
            # doc.user = user
            # doc.first_name = user_form.cleaned_data['first_name']
            # doc.last_name = user_form.cleaned_data['last_name']
            # doc.save()

            # doc_form = DoctorProfile(request.POST, isinstance=user.doc)

            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password1']
            user=authenticate(username=username, password=password)

            messages.success(request,"Doctor Registred Successfully!")
            login(request,user)
            
            # doc_form = DoctorsProfileForm()
            redirect('home')


        else:
            print(user_form.errors)
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            context = {'form': user_form} 
    else:
        user_form = UserForm()

    context = {
       
        'user_form':user_form
    }
    return render(request, 'doctors/doctors_registration_page.html', context)


def DoctorLogin(request):
    if request.method == 'POST':
        user_form  = UserLoginForm(request.POST)

        if user_form.is_valid():
            user = user_form.get_user()
            if user is not None:
                login(request, user)
                redirect('home')
    else:
        user_form  = UserLoginForm()
    
    return render(request, 'doctors/doctors_login.html', {'user_form':user_form})
                

def Posts(request):
    pass

def PatientAppointments(request):
    pass

def Doctors(request):
    pass

def Messages(request):
    pass

def DoctorLogout(request):
    logout(request)
    next_page = request.GET.get('next', 'DoctorLogin')
    return redirect(reverse(next_page))
    