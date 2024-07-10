from django.test import TestCase, Client
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor
from unittest.mock import patch, MagicMock
import json


class PatientViewsCoverageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='pview', password='pass', email='pview@example.com')
        self.patient = Patient.objects.create(
            user=self.user, fname='Pat', lname='View', email='pview@example.com'
        )
        self.doc_user = User.objects.create_user(username='docview', password='pass')
        self.doctor = Doctor.objects.create(user=self.doc_user, first_name='Doc', last_name='View')

    def test_patient_login_success(self):
        resp = self.client.post('/patients/PatientLogin/', {
            'username': 'pview',
            'password': 'pass',
        })
        self.assertEqual(resp.status_code, 302)

    def test_patient_login_get(self):
        resp = self.client.get('/patients/PatientLogin/')
        self.assertEqual(resp.status_code, 200)

    def test_patient_profile_get_and_post(self):
        self.client.login(username='pview', password='pass')
        self.assertEqual(self.client.get('/patients/PatientProfile/').status_code, 200)
        resp = self.client.post('/patients/PatientProfile/', {
            'fname': 'Updated',
            'lname': 'Name',
            'email': 'updated@example.com',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'contact_number': '1234567890',
            'address': '123 Main St',
            'emergency_contact_name': 'EC',
            'emergency_contact_phone': '0987654321',
        })
        self.assertIn(resp.status_code, (200, 302))

    def test_gemini_chat_post_with_session(self):
        self.client.login(username='pview', password='pass')
        from patients import gemini
        chat = gemini.Chat()
        session = self.client.session
        session['chat'] = chat.serialize()
        session.save()
        with patch.object(gemini.Chat, 'gemini_new_request', return_value='mock reply'):
            resp = self.client.post('/patients/GeminiChat/', {'question': 'headache'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['response'], 'mock reply')

    def test_gemini_chat_post_follow_up(self):
        self.client.login(username='pview', password='pass')
        from patients import gemini
        chat = gemini.Chat()
        chat.messages = [{'role': 'user', 'parts': ['hi']}]
        chat.response = 'hello'
        session = self.client.session
        session['chat'] = chat.serialize()
        session.save()
        with patch.object(gemini.Chat, 'gemini_request', return_value='follow up'):
            resp = self.client.post('/patients/GeminiChat/', {'question': 'more'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['response'], 'follow up')

    def test_add_diagnostic_results(self):
        self.client.login(username='docview', password='pass')
        resp_get = self.client.get(f'/patients/add-diagnostic-results/{self.patient.id}')
        self.assertEqual(resp_get.status_code, 200)
        resp_post = self.client.post(
            f'/patients/add-diagnostic-results/{self.patient.id}',
            {
                'diagnosis': 'Flu',
                'symptoms': 'Fever',
                'treatment': 'Rest',
                'prescription': 'None',
                'notes': 'Monitor',
            },
        )
        self.assertEqual(resp_post.status_code, 302)
        self.assertTrue(self.patient.medical_histories.filter(diagnosis='Flu').exists())

    def test_patient_logout(self):
        self.client.login(username='pview', password='pass')
        resp = self.client.get('/patients/PatientLogout/')
        self.assertEqual(resp.status_code, 302)
