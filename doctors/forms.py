from django import forms
from .models import Doctor
from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator, MinLengthValidator
from .models import Post

class UserForm(UserCreationForm):
    password1= forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        validators=[MinLengthValidator(8)]
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        validators=[MinLengthValidator(8)]
    )

    email = forms.EmailField(validators=[EmailValidator()])
    class Meta:
        model = User
        fields = ( 'username','email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
            'password': forms.PasswordInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
            'password2': forms.PasswordInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
            
        }


# class DoctorsProfileForm(forms.Form):
    
#     class Meta:
#         model = Doctor
#         fields = ['first_name', 'last_name','national_id_or_passport_image','phone_number','medical_licence','passport_or_id_number','date_issued','expiry_date','date_of_birth','specialization']


from django import forms
from .models import Doctor

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'specialization', 'phone_number', 'photo', 'medical_licence', 'passport_or_id_number', 'date_issued', 'expiry_date', 'date_of_birth', 'national_id_or_passport_image', 'city','region','languages','years_of_experience']
         
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),

            'date_issued': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }



class UserLoginForm(forms.Form):
  username = forms.CharField(label="Username", max_length=150)
  password = forms.CharField(label="Password", widget=forms.PasswordInput())

  def clean(self):
    cleaned_data = super(UserLoginForm, self).clean()
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')

    if not username:
      raise forms.ValidationError('Please enter your username.')
    if not password:
      raise forms.ValidationError('Please enter your password.')

    return cleaned_data
  

  #POSTS SECTION
class ThumbsUpForm(forms.Form):
    pass



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image_main', 'image1', 'image2', 'image3', 'content']