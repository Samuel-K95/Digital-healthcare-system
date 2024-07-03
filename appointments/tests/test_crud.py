from django.test import TestCase
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from django.utils import timezone


class AppointmentCrudTests(TestCase):
    def test_create_update_delete_appointment(self):
        udoc = User.objects.create_user(username='doccrud', password='pass')
        doc = Doctor.objects.create(user=udoc)
        upat = User.objects.create_user(username='patcrud', password='pass')
        pat = Patient.objects.create(user=upat, fname='P', lname='C', email='pc@example.com')
        appt = Appointment.objects.create(doctor=doc, patient=pat, appointment_date=timezone.now())
        self.assertIsNotNone(appt.id)
        appt.status = 'accepted'
        appt.save()
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'accepted')
        appt.delete()
        self.assertFalse(Appointment.objects.filter(id=appt.id).exists())
