from django import forms
from .models import Appointment
import datetime 
from django.utils import timezone



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'appointment_date',
            'additional_requests',            
        ]
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'date'})
            }
        



def clean_appointment_date(self):
    appointment_date = self.cleaned_data['appointment_date'].replace(tzinfo=None)
    now = datetime.datetime.now()
    if appointment_date < now:
        raise forms.ValidationError("Appointment date can't be set in the past.")
    return appointment_date