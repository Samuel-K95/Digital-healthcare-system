from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from rating.models import Rating
from rating.views import average_star_rating
from django.utils import timezone
from datetime import timedelta


class RatingViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_doc = User.objects.create_user(username='rdoc', password='pass')
        self.doctor = Doctor.objects.create(user=self.user_doc, first_name='R', last_name='Doc')
        self.user_pat = User.objects.create_user(username='rpat', password='pass')
        self.patient = Patient.objects.create(user=self.user_pat, fname='P', lname='T', email='p@t.com')

    def test_average_star_rating(self):
        # simple average computation
        self.assertEqual(average_star_rating(4, 5, 1), 4)

    def test_rate_doctor_get_renders(self):
        self.client.login(username='rpat', password='pass')
        resp = self.client.get(f'/Rating/rate_doctor/{self.doctor.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_rate_doctor_post_without_appointment_redirects(self):
        self.client.login(username='rpat', password='pass')
        resp = self.client.post(f'/Rating/rate_doctor/{self.doctor.id}/', data={'score': 5, 'review': 'Good'})
        self.assertEqual(resp.status_code, 302)

    def test_rate_doctor_post_with_appointment_creates_rating(self):
        # create an appointment linking patient and doctor
        Appointment.objects.create(doctor=self.doctor, patient=self.patient, appointment_date=timezone.now())
        self.client.login(username='rpat', password='pass')
        resp = self.client.post(f'/Rating/rate_doctor/{self.doctor.id}/', data={'score': 5, 'review': 'Great'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Rating.objects.filter(rated_doctor=self.doctor, rater_patient=self.patient).exists())
