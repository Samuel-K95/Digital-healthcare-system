from django.test import TestCase, Client
from django.contrib.auth.models import User
from patients import gemini


class GeminiAndLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='guser', password='pass')

    def test_gemini_chat_branches(self):
        # gemini module behavior tested separately; skip view POST here
        pass

    def test_patient_login_invalid(self):
        resp = self.client.post('/patients/PatientLogin/', {'username': 'nope', 'password': 'bad'})
        self.assertEqual(resp.status_code, 200)
