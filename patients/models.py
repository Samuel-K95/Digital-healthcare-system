from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname  = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    age= models.IntegerField(null=True)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True)
    contact_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    date_of_birth = models.DateField(null=True)
    emergency_contact = models.CharField(max_length=100, null=True)

    def create_user(self):
        pass

    def __str__(self):
        return self.fname + self.lname

class MedicalHisory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    details = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f'Patients name: {self.patient.name} diagnosis: {self.diagnosis}'