from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Doctor
from .forms import DoctorProfileForm, UserLoginForm, UserForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
#login and logout

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
#login and logout


def DoctorDetail(request,pk):
    doctors = Doctor.objects.get(id=pk)
    context = {
        'doctors' : doctors  
    }
    
    return render(request, 'doctors/dashboard.html', context)



def DoctorProfile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('DoctorProfile')
    else:
        form = DoctorProfileForm(instance=doctor)
    return render(request, 'doctors/doctor_profile.html', {'form': form, 'doc':doctor})

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
            return redirect('DoctorProfile')


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
    username = request.POST['username']
    password = request.POST['password1']

    user = authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('DoctorProfile')  
    else:
      # Login failed
      messages.error(request, 'Invalid username or password!')
      return redirect('DoctorLogin')
  
  return render(request, 'doctors/doctors_login.html')
                


from django.db.models import Q

def BrowseDoctors(request):

    if(request.user.is_authenticated):
        template = 'doctors/search_and_book_doctors.html'
    else:
        template = 'doctors/browse_doctors.html'


    query = request.GET.get('query', '')
    city = request.GET.get('city', '')
    region = request.GET.get('region', '')
    country = request.GET.get('country', '')
    years_of_experience = request.GET.get('years_of_experience', '')
    languages = request.GET.get('languages', '')
    doctor_type = request.GET.get('doctor_type', '')
    rating = request.GET.get('rating', '')

    doctors = Doctor.objects.filter(verification_status='approved')

    # Filter by city
    if city:
        doctors = doctors.filter(city__iexact=city)

    # Filter by region
    if region:
        doctors = doctors.filter(region__iexact=region)


    # Filter by years of experience
    if years_of_experience:
        doctors = doctors.filter(years_of_experience__gte=years_of_experience)

    # Filter by languages
    if languages:
        doctors = doctors.filter(languages__icontains=languages)

    # Filter by doctor type
    if doctor_type:
        doctors = doctors.filter(doctor_type__iexact=doctor_type)

    # Filter by rating
    if rating:
        doctors = doctors.filter(rating__gte=rating)

    # Search by query
    if query:
        doctors = doctors.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(specialization__icontains=query)|
            Q(city__icontains=query)|
            Q(region__icontains=query)|
            Q(languages__icontains=query)
        )

    # Order by rating (descending)
    doctors = doctors.order_by('-rating')

    unique_years_of_experience = Doctor.objects.values_list('years_of_experience', flat=True).distinct()
    unique_cities= Doctor.objects.values_list('city', flat=True).distinct()

    context = {
        'doctors': doctors,
        'query': query,
        'city': city,
        'region': region,
        'years_of_experience': years_of_experience,
        'languages': languages,
        'doctor_type': doctor_type,
        'rating': rating,
        'unique_years_of_experience':unique_years_of_experience,
        'unique_cities':unique_cities,
    }

    return render(request, template, context)


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
    