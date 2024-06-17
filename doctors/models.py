from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name  = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    #verification status
    VERIFICATION_TYPE_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        
    )
    verification_message = models.TextField(max_length=1000, blank=True, null=True, default="")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_TYPE_CHOICES, blank=True, null=True)



    # verification details
    national_id_or_passport_image = models.ImageField(upload_to='doctors/verification', blank=True, null=True)
    phone_number = models.IntegerField(blank=True, default=True)
    photo = models.ImageField(upload_to='doctors/account',  null=True, blank=True)
    medical_licence = models.ImageField(upload_to='doctors/verification',  null=True, blank=True)
    passport_or_id_number = models.IntegerField(blank=True, null=True)
    date_issued = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    #specialization
    specialization = models.TextField(max_length=1000, blank=True, null=True, default="")

    #ratings
    rating = models.FloatField(default=0.0, null=True, blank=True)
    rating_counter = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.f_name} {self.l_name}"

