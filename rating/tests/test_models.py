from django.test import TestCase
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from rating.models import Rating
from django.utils import timezone


class RatingModelTests(TestCase):
    def test_rating_str(self):
        udoc = User.objects.create_user(username='docrat', password='pass')
        doc = Doctor.objects.create(user=udoc, first_name='Doc', last_name='Tor')
        upat = User.objects.create_user(username='patrat', password='pass')
        pat = Patient.objects.create(user=upat, fname='R', lname='At', email='r@a.com')
        r = Rating.objects.create(rated_doctor=doc, rater_patient=pat, score=5)
        self.assertIn('5 Stars', str(r))
