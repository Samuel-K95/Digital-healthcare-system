from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
import datetime


class AppointmentsRescheduleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doc_user = User.objects.create_user(username='drs', password='pass')
        self.pat_user = User.objects.create_user(username='pts', password='pass')
        self.doctor = Doctor.objects.create(user=self.doc_user, first_name='DrS', verification_status='approved')
        self.patient = Patient.objects.create(user=self.pat_user, fname='F', lname='L', email='e@e.com')
        from django.core.files.base import ContentFile
        self.doctor.photo.save('dp.jpg', ContentFile(b''), save=True)
        self.appt = Appointment.objects.create(patient=self.patient, doctor=self.doctor, appointment_date=datetime.datetime.now() + datetime.timedelta(days=1))

    def test_reschedule_get_and_post(self):
        self.client.login(username='drs', password='pass')
        resp_get = self.client.get(f'/appointments/reschedule_appointment/{self.appt.id}/')
        self.assertEqual(resp_get.status_code, 200)
        new_date = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        resp_post = self.client.post(f'/appointments/reschedule_appointment/{self.appt.id}/', {'appointment_date': new_date})
        self.assertIn(resp_post.status_code, (200,302))

    def test_edit_appointment(self):
        self.client.login(username='drs', password='pass')
        resp = self.client.post(f'/appointments/edit_appointment/{self.appt.id}/', {'appointment_date': (datetime.datetime.now()+datetime.timedelta(days=2)).strftime('%Y-%m-%d'), 'additional_requests': 'ok'})
        self.assertIn(resp.status_code, (200,302))

    def test_delete_appointment(self):
        self.client.login(username='drs', password='pass')
        resp = self.client.get(f'/appointments/delete_appointment/{self.appt.id}/')
        self.assertIn(resp.status_code, (200,302))
        self.assertFalse(Appointment.objects.filter(id=self.appt.id).exists())
