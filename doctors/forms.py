from django import forms
from .models import Doctor
from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator, MinLengthValidator

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


class DoctorsProfileForm(forms.Form):
    
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
        }






class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password= forms.CharField(widget=forms.PasswordInput)
    user = None
    
    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get('username')
        password1= cleaned_data.get('password1')
        if user_name and password1:
            user = authenticate(username=user_name, password=password)
            self.user = user

            if user is None:
                raise forms.ValidationError("invalid username")
            return cleaned_data
        else:
            raise forms.ValidationError("invalid username or password")
        
    def get_user(self):
        return self.user