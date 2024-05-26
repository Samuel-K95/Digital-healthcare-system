from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patient

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('fname', 'lname')
