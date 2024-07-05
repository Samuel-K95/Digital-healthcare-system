from django.test import TestCase, Client
from django.contrib.auth.models import User
from patients.models import Patient


class PatientBasicViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='puser', password='pass')
        self.patient = Patient.objects.create(user=self.user, fname='F', lname='L', email='f@l.com')

    def test_index(self):
        resp = self.client.get('/patients/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('index', resp.content.decode().lower())

    def test_patient_dashboard(self):
        resp = self.client.get(f'/patients/PatientDashboard/{self.user.pk}')
        self.assertEqual(resp.status_code, 200)

    def test_patient_logout_redirects(self):
        self.client.login(username='puser', password='pass')
        resp = self.client.get('/patients/PatientLogout/')
        self.assertIn(resp.status_code, (301,302))
