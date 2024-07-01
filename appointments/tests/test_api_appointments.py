from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from django.utils import timezone
from datetime import timedelta
import json


class ApiAppointmentsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_doctor = User.objects.create_user(username='docapi', password='pass')
        self.doctor = Doctor.objects.create(user=self.user_doctor)
        self.user_patient = User.objects.create_user(username='patapi', password='pass')
        self.patient = Patient.objects.create(user=self.user_patient, fname='Test', lname='Patient', email='papi@example.com')

    def test_available_slots_and_create(self):
        start = (timezone.now() + timedelta(minutes=5)).replace(second=0, microsecond=0)
        end = start + timedelta(hours=1)
        resp = self.client.get(f'/appointments/api/doctors/{self.doctor.id}/availability/?start={start.isoformat()}&end={end.isoformat()}&duration=30')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('slots', data)
        slots = data['slots']
        self.assertTrue(len(slots) >= 1)

        # book first slot
        slot = slots[0]['start']
        resp2 = self.client.post('/appointments/api/appointments/', data=json.dumps({'doctor_id': self.doctor.id, 'patient_id': self.patient.id, 'slot_start': slot, 'duration': 30}), content_type='application/json')
        self.assertIn(resp2.status_code, (200,201))
        data2 = resp2.json()
        self.assertIn('appointment_id', data2)
