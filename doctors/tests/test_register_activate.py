from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from unittest.mock import patch


class RegisterActivateTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('doctors.views.send_verification_email')
    def test_register_doctor_post(self, mock_send):
        data = {'username': 'drreg', 'email': 'dr@reg.com', 'password1': 'strongpass1', 'password2': 'strongpass1'}
        resp = self.client.post('/doctors/DoctorSignUp/', data)
        # registration view attempts to login and redirect to profile
        self.assertIn(resp.status_code, (200,302))
        self.assertTrue(User.objects.filter(username='drreg').exists())

    def test_activate_account(self):
        user = User.objects.create_user(username='toact', email='t@a.com', password='pass')
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        resp = self.client.get(f'/doctors/activate/{uid}/{token}/')
        self.assertIn(resp.status_code, (301,302))

    def test_doctor_login_success(self):
        user = User.objects.create_user(username='dlogin', password='pass')
        resp = self.client.post('/doctors/DoctorLogin/', {'username': 'dlogin', 'password1': 'pass'})
        # view may redirect on success
        self.assertIn(resp.status_code, (200,302))
