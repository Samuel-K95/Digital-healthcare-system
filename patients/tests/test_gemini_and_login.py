from django.test import TestCase, Client
from django.contrib.auth.models import User
from patients import gemini


class GeminiAndLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='guser', password='pass')

    def test_gemini_chat_branches(self):
        # empty messages -> gemini_new_request
        chat = gemini.Chat()
        self.client.session['chat'] = chat.serialize()
        self.client.session.save()
        resp = self.client.post('/patients/GeminiChat/', {'question': 'hello'})
        # returns JSON or redirect depending on implementation
        self.assertIn(resp.status_code, (200,302))

    def test_patient_login_invalid(self):
        resp = self.client.post('/patients/PatientLogin/', {'username': 'nope', 'password': 'bad'})
        self.assertEqual(resp.status_code, 200)
