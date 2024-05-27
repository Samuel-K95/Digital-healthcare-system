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
    def get_user(self):
        return self.user

