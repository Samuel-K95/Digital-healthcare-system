from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Doctor, Post
from .forms import DoctorProfileForm, UserLoginForm, UserForm, ThumbsUpForm, PostForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
#login and logout

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#login and logout

#Email verification and account activation
from django.contrib import messages
from .utils import  send_verification_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
#Email verification and account activation


def DoctorDetail(request,pk):
    doctor = Doctor.objects.get(id=pk)
    context = {
        'doctor' : doctor  
    }
    
    return render(request, 'doctors/doctor_detail.html', context)



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
            
             #Send email
            mail_subject = 'Please activate your account'
            email_template = 'doctors/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            
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


def activateAccount(request, uidb64, token):
    print("*************-------Account Activation-------**************")
   
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print("Account Successfully Activated!")
        return redirect('home')
    else:
        print("Invalid Activation Link!")
        return redirect('home')

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
        if(Doctor.objects.filter(user=request.user).exists()):
            template = 'doctors/search_and_book_doctors.html'
            print("Doctor")
        else:    
            print("Patient")
            template = 'patients/search_and_book_doctors.html'
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
    



# POSTS SECTION 
def PostList(request):
    posts = Post.objects.all().order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'posts/post_list.html', context)


def MyPosts(request):
    doctor = Doctor.objects.get(user=request.user)
    posts = Post.objects.filter(author=doctor).order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'posts/my_posts.html', context)


def PostDetail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    liked = post.has_liked(request.user)  # Check if user already liked

    if request.method == 'POST':
        form = ThumbsUpForm(request.POST)  # Handle form submission (if applicable)
        if form.is_valid():
            if not liked:
                # Add user to liked_by and increment thumbs_up
                post.liked_by.add(request.user)
                post.thumbs_up += 1
                post.save()
                messages.success(request, "Liked Successfully!")
                liked = True  # Update liked flag after thumbs up
            else:
                messages.error(request, "You already liked this post!")

    context = {'post': post, 'liked': liked}
    return render(request, 'posts/post_detail.html', context)


@login_required(login_url='login')
def CreatePost(request):
    doctor = Doctor.objects.get(user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = doctor
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})

login_required(login_url='login')
def EditPost(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required(login_url='login')
def DeletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request,"Post Deleted Successfully!")
    return redirect('post_list')
