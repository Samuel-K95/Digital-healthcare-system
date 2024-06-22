from django.db import models
from django.contrib.auth.models import User
import datetime 
from doctors.models import Doctor


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname  = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    date_of_birth = models.DateField(null=True)
    age= models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True)
    contact_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True)


    def create_user(self):
        pass
    
    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = datetime.date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            self.age = age
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fname + " " + self.lname

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_medical_histories', null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical History for {self.patient.fname} {self.patient.lname}"