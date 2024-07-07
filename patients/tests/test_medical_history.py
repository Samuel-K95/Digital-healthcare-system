from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient, MedicalHistory


class MedicalHistoryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doc_user = User.objects.create_user(username='drmh', password='pass')
        self.pat_user = User.objects.create_user(username='pmh', password='pass')
        self.doctor = Doctor.objects.create(user=self.doc_user, first_name='DrMH', verification_status='approved')
        self.patient = Patient.objects.create(user=self.pat_user, fname='F', lname='L', email='e@e.com')
        from django.core.files.base import ContentFile
        self.doctor.photo.save('dp.jpg', ContentFile(b''), save=True)

    def test_view_medical_history(self):
        resp = self.client.get(f'/patients/medical-history/{self.patient.id}')
        self.assertEqual(resp.status_code, 200)

    def test_add_diagnostic_results(self):
        self.client.login(username='drmh', password='pass')
        data = {'diagnosis': 'D', 'symptoms': 'S', 'treatment': 'T', 'prescription': 'P', 'notes': 'N'}
        resp = self.client.post(f'/patients/add-diagnostic-results/{self.patient.id}', data)
        self.assertIn(resp.status_code, (200,302))
        self.assertTrue(MedicalHistory.objects.filter(patient=self.patient).exists())
