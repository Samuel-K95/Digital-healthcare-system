from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    # verification status
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    verification_message = models.TextField(max_length=1000, blank=True, null=True, default="")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, blank=True, null=True)

    # verification details
    national_id_or_passport_image = models.ImageField(upload_to='doctors/verification', blank=True, null=True)
    phone_number = models.CharField(max_length=14, default=True, blank=True, null=True)
    photo = models.ImageField(upload_to='doctors/account', null=True, blank=True)
    medical_licence = models.ImageField(upload_to='doctors/verification', null=True, blank=True)
    passport_or_id_number = models.CharField(max_length=20, blank=True, null=True)
    date_issued = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # specialization
    specialization = models.CharField(max_length=1000, blank=True, null=True, default="")


    city = models.CharField(max_length=100,  blank=True, null=True)

    REGION_CHOICES = (
        ("Afar", "Afar"),
        ("Amhara", "Amhara"),
        ("Benishangul-Gumuz", "Benishangul-Gumuz"),
        ("Gambela", "Gambela"),
        ("Harari", "Harari"),
        ("Oromia", "Oromia"),
        ("Somali", "Somali"),
        ("Southern Nations, Nationalities, and Peoples'", "Southern Nations, Nationalities, and Peoples'"),
        ("Tigray", "Tigray"),
        ("Sidama", "Sidama"),
        ("Nuer", "Nuer"),
        ("Wolayita", "Wolayita"),
    )
    region = models.CharField(max_length=100, choices=REGION_CHOICES, blank=True, null=True)

    country = models.CharField(max_length=100, blank=True, null=True)

    # Years of experience
    YEARS_OF_EXPERIENCE_CHOICES = (
        ("less than 1", "Less than 1 year"),
        ("1-3", "1-3 years"),
        ("3-5", "3-5 years"),
        ("more than 5", "More than 5 years"),
    )
    years_of_experience = models.CharField(max_length=20, choices=YEARS_OF_EXPERIENCE_CHOICES, blank=True, null=True)

    # Languages
    languages = models.CharField(max_length=200, blank=True, null=True)
    

    # ratings
    rating = models.FloatField(default=0.0, null=True, blank=True)
    rating_counter = models.IntegerField(default=0, null=True, blank=True)

   
    def __str__(self):
        return f"Username: {self.user} || Full Name: {self.first_name} {self.last_name}"

