from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
import datetime
from unittest.mock import patch


class AppointmentsMoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doc_user = User.objects.create_user(username='docm', password='pass')
        self.pat_user = User.objects.create_user(username='patm', password='pass')
        self.doctor = Doctor.objects.create(user=self.doc_user, first_name='DocM', verification_status='approved')
        self.patient = Patient.objects.create(user=self.pat_user, fname='P', lname='M', email='p@m.com')
        from django.core.files.base import ContentFile
        self.doctor.photo.save('dp.jpg', ContentFile(b''), save=True)

    def test_schedule_appointment_post(self):
        # login as patient
        self.client.login(username='patm', password='pass')
        future = (datetime.datetime.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
        data = {'appointment_date': future, 'additional_requests': 'None'}
        resp = self.client.post(f'/appointments/schedule_appointment/{self.doctor.id}/', data)
        self.assertIn(resp.status_code, (301,302))
        self.assertTrue(Appointment.objects.filter(patient=self.patient, doctor=self.doctor).exists())

    def test_confirm_appointment_sends_email(self):
        appt = Appointment.objects.create(patient=self.patient, doctor=self.doctor, appointment_date=datetime.datetime.now())
        self.client.login(username='docm', password='pass')
        with patch('appointments.views.send_mail') as mock_send:
            resp = self.client.get(f'/appointments/confirm_appointment/{appt.id}/')
            self.assertIn(resp.status_code, (301,302))
            self.assertTrue(mock_send.called)
