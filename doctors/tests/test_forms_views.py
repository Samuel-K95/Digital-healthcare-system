from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.forms import DoctorProfileForm
from doctors.models import Doctor
from rating.models import Rating
from django.utils import timezone
from datetime import date, timedelta


class DoctorFormAndViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='dvuser', password='pass', email='dv@example.com')
        self.doctor = Doctor.objects.create(user=self.user, first_name='A', last_name='B', verification_status='approved')
        from django.core.files.base import ContentFile
        self.doctor.photo.save('p.jpg', ContentFile(b'p'), save=True)

    def test_clean_date_of_birth_future(self):
        future = date.today() + timedelta(days=10)
        form = DoctorProfileForm(data={'date_of_birth': future})
        self.assertFalse(form.is_valid())
        self.assertIn('Date of birth cannot be a future date.', str(form.errors))

    def test_clean_date_of_birth_too_young(self):
        young = date.today() - timedelta(days=365*16)
        form = DoctorProfileForm(data={'date_of_birth': young})
        self.assertFalse(form.is_valid())
        self.assertIn('You must be 18 years old', str(form.errors))

    def test_clean_date_issued_future(self):
        future = date.today() + timedelta(days=5)
        form = DoctorProfileForm(data={'date_issued': future})
        self.assertFalse(form.is_valid())
        self.assertIn('Issue date cannot be a future date.', str(form.errors))

    def test_clean_expiry_before_issue(self):
        issued = date.today()
        expiry = date.today() - timedelta(days=1)
        form = DoctorProfileForm(data={'date_issued': issued, 'expiry_date': expiry})
        self.assertFalse(form.is_valid())
        self.assertIn('Expiry date cannot be in the past.', str(form.errors))

    def test_doctor_detail_view(self):
        from patients.models import Patient
        userp = User.objects.create_user(username='p_rater', password='pass')
        patient = Patient.objects.create(user=userp, fname='R', lname='P', email='r@p.com')
        Rating.objects.create(rated_doctor=self.doctor, rater_patient=patient, score=4)
        resp = self.client.get(f'/doctors/DoctorDetail/{self.doctor.id}')
        self.assertEqual(resp.status_code, 200)

    def test_doctor_logout_redirects(self):
        self.client.login(username='dvuser', password='pass')
        resp = self.client.get('/doctors/DoctorLogout/')
        # should redirect
        self.assertIn(resp.status_code, (302, 301))
