from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from django.utils import timezone
from datetime import timedelta
import json


class ApiErrorPathTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doc_user = User.objects.create_user(username='docerr', password='pass')
        self.doctor = Doctor.objects.create(user=self.doc_user)
        self.pat_user = User.objects.create_user(username='paterr', password='pass')
        self.patient = Patient.objects.create(user=self.pat_user, fname='E', lname='R', email='e@r.com')
        self.other = User.objects.create_user(username='othererr', password='pass')

    def test_availability_missing_params(self):
        resp = self.client.get(f'/appointments/api/doctors/{self.doctor.id}/availability/')
        self.assertEqual(resp.status_code, 400)

    def test_availability_invalid_datetime(self):
        resp = self.client.get(
            f'/appointments/api/doctors/{self.doctor.id}/availability/?start=bad&end=also-bad'
        )
        self.assertEqual(resp.status_code, 400)

    def test_availability_doctor_not_found(self):
        start = (timezone.now() + timedelta(hours=1)).isoformat()
        end = (timezone.now() + timedelta(hours=2)).isoformat()
        resp = self.client.get(f'/appointments/api/doctors/99999/availability/?start={start}&end={end}')
        self.assertEqual(resp.status_code, 404)

    def test_create_invalid_json(self):
        self.client.login(username='paterr', password='pass')
        resp = self.client.post(
            '/appointments/api/appointments/',
            data='not-json',
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_missing_fields(self):
        self.client.login(username='paterr', password='pass')
        resp = self.client.post(
            '/appointments/api/appointments/',
            data=json.dumps({'doctor_id': self.doctor.id}),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_unauthenticated(self):
        slot = (timezone.now() + timedelta(days=1)).isoformat()
        resp = self.client.post(
            '/appointments/api/appointments/',
            data=json.dumps({
                'doctor_id': self.doctor.id,
                'patient_id': self.patient.id,
                'slot_start': slot,
            }),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 401)

    def test_create_forbidden_for_other_user(self):
        self.client.login(username='othererr', password='pass')
        slot = (timezone.now() + timedelta(days=1)).replace(second=0, microsecond=0).isoformat()
        resp = self.client.post(
            '/appointments/api/appointments/',
            data=json.dumps({
                'doctor_id': self.doctor.id,
                'patient_id': self.patient.id,
                'slot_start': slot,
            }),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 403)

    def test_create_doctor_or_patient_not_found(self):
        self.client.login(username='paterr', password='pass')
        slot = (timezone.now() + timedelta(days=1)).isoformat()
        resp = self.client.post(
            '/appointments/api/appointments/',
            data=json.dumps({
                'doctor_id': 99999,
                'patient_id': self.patient.id,
                'slot_start': slot,
            }),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 404)

    def test_create_slot_conflict(self):
        slot = (timezone.now() + timedelta(days=2)).replace(second=0, microsecond=0)
        from appointments.models import Appointment
        Appointment.objects.create(doctor=self.doctor, patient=self.patient, appointment_date=slot)
        self.client.login(username='paterr', password='pass')
        resp = self.client.post(
            '/appointments/api/appointments/',
            data=json.dumps({
                'doctor_id': self.doctor.id,
                'patient_id': self.patient.id,
                'slot_start': slot.isoformat(),
            }),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 409)

    def test_create_invalid_slot_start(self):
        self.client.login(username='paterr', password='pass')
        resp = self.client.post(
            '/appointments/api/appointments/',
            data=json.dumps({
                'doctor_id': self.doctor.id,
                'patient_id': self.patient.id,
                'slot_start': 'not-a-date',
            }),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)
