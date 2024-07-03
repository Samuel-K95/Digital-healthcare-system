from django.test import TestCase
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from access.policy import get_role, can_create_appointment, can_view_appointment, can_edit_appointment
from django.utils import timezone


class PolicyTests(TestCase):
    def setUp(self):
        self.user_doc = User.objects.create_user(username='docpol', password='pass')
        self.user_pat = User.objects.create_user(username='patpol', password='pass')
        self.doctor, _ = Doctor.objects.get_or_create(user=self.user_doc)
        self.patient = Patient.objects.create(user=self.user_pat, fname='P', lname='Q', email='p@q.com')

    def test_role_resolution(self):
        self.assertEqual(get_role(self.user_doc), 'doctor')
        self.assertEqual(get_role(self.user_pat), 'patient')

    def test_patient_can_create_own(self):
        self.assertTrue(can_create_appointment(self.user_pat, self.doctor, self.patient))

    def test_doctor_can_create_for_self(self):
        self.assertTrue(can_create_appointment(self.user_doc, self.doctor, self.patient))

    def test_view_permissions(self):
        appt = Appointment.objects.create(doctor=self.doctor, patient=self.patient, appointment_date=timezone.now())
        self.assertTrue(can_view_appointment(self.user_doc, appt))
        self.assertTrue(can_view_appointment(self.user_pat, appt))

    def test_edit_rules(self):
        appt = Appointment.objects.create(doctor=self.doctor, patient=self.patient, appointment_date=timezone.now(), status='pending')
        self.assertTrue(can_edit_appointment(self.user_pat, appt))
        appt.status = 'accepted'
        appt.save()
        self.assertFalse(can_edit_appointment(self.user_pat, appt))
