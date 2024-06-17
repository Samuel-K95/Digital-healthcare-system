from django import forms
from .models import Doctor

class DoctorsRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'user',
            'f_name',
            'l_name',
            'email',
            'national_id_or_passport_image',
            'passport_or_id_number',
            'date_of_birth',
            'date_issued',
            'expiry_date',
            'verification_message',
            'verification_status',        
            'phone_number',
            'medical_licence',
            'specialization'
            ]
        
        widgets = {
            'date_issued': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
