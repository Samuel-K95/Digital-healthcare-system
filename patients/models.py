from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age= models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    emergency_contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MedicalHisory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    details = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f'Patients name: {self.patient.name} diagnosis: {self.diagnosis}'