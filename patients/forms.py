from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Patient

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('fname', 'lname')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    user = None
    
    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if user_name and password:
            user = authenticate(username=user_name, password=password)
            self.user = user

            if user is None:
                raise forms.ValidationError("invalid username")
            return cleaned_data
        else:
            raise forms.ValidationError("invalid username or password")
        
    def get_user(self):
        return self.user



class GeminiChatForm(forms.Form):
    question = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': 'Type your message here...'})
    )


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['fname', 'lname', 'email', 'contact_number', 'gender', 'address', 'emergency_contact_name', 'emergency_contact_phone', 'date_of_birth']
         
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),
            'lname': forms.TextInput(attrs={'class': 'w-full text-sm px-4 py-3 rounded outline-none border-2 focus:border-blue-500'}),

            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

