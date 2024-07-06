from django.test import TestCase, Client
from django.contrib.auth.models import User
from patients.models import Patient


class PatientSignupProfileTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_patient_signup(self):
        data = {'username': 'newp', 'email': 'n@p.com', 'password1': 'strongpass1', 'password2': 'strongpass1', 'fname': 'FN', 'lname': 'LN'}
        resp = self.client.post('/patients/PatientSignUp/', data)
        # Should redirect to dashboard
        self.assertIn(resp.status_code, (301,302))
        self.assertTrue(User.objects.filter(username='newp').exists())

    def test_patient_profile_update(self):
        u = User.objects.create_user(username='pup', password='pass')
        patient = Patient.objects.create(user=u, fname='F', lname='L', email='e@e.com')
        self.client.login(username='pup', password='pass')
        resp = self.client.post('/patients/PatientProfile/', {'fname': 'X', 'lname': 'Y', 'email': 'x@y.com'})
        self.assertIn(resp.status_code, (200,302))
        patient.refresh_from_db()
        self.assertEqual(patient.fname, 'X')
