from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
import datetime


class AppointmentsViewsBasicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor_user = User.objects.create_user(username='docu', password='pass')
        self.patient_user = User.objects.create_user(username='patu', password='pass')
        self.doctor = Doctor.objects.create(user=self.doctor_user, first_name='Doc', verification_status='approved')
        self.patient = Patient.objects.create(user=self.patient_user, fname='P', lname='L', email='p@l.com')

    def test_schedule_requires_login(self):
        resp = self.client.get(f'/appointments/schedule_appointment/{self.doctor.id}/')
        self.assertIn(resp.status_code, (301,302))

    def test_join_the_call_redirects(self):
        appt = Appointment.objects.create(patient=self.patient, doctor=self.doctor, appointment_date=datetime.datetime.now())
        self.client.login(username='patu', password='pass')
        resp = self.client.get(f'/appointments/join_the_call/{appt.id}')
        self.assertIn(resp.status_code, (301,302))
        self.assertIn(str(appt.id), resp.url)
