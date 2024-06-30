from django.test import TestCase
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.services.scheduler import find_available_slots, book_slot_atomic
from django.utils import timezone
from datetime import timedelta


class SchedulerTests(TestCase):
    def setUp(self):
        self.user_doctor = User.objects.create_user(username='doc1', password='pass')
        self.doctor = Doctor.objects.create(user=self.user_doctor)
        self.user_patient = User.objects.create_user(username='pat1', password='pass')
        self.patient = Patient.objects.create(user=self.user_patient, fname='Test', lname='Patient', email='p@example.com')

    def test_find_slots_empty_schedule(self):
        start = timezone.now()
        end = start + timedelta(hours=2)
        slots = find_available_slots(self.doctor, start, end, duration_minutes=30)
        # Expect 4 slots in 2 hours with 30-minute duration
        self.assertEqual(len(slots), 4)

    def test_book_slot_and_conflict(self):
        start = (timezone.now() + timedelta(minutes=5)).replace(second=0, microsecond=0)
        # Book a slot
        appt = book_slot_atomic(self.doctor, self.patient, start, duration_minutes=30)
        self.assertIsNotNone(appt.id)
        # Attempt to book same slot should raise
        with self.assertRaises(ValueError):
            book_slot_atomic(self.doctor, self.patient, start, duration_minutes=30)
