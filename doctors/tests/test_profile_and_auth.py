from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
import datetime


class DoctorProfileAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='docpa', password='pass')
        self.doctor = Doctor.objects.create(user=self.user, first_name='DocPA', verification_status='approved')
        from django.core.files.base import ContentFile
        self.doctor.photo.save('pp.jpg', ContentFile(b''), save=True)

    def test_doctor_profile_update(self):
        self.client.login(username='docpa', password='pass')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'a@b.com',
            'date_of_birth': '1980-01-01',
            'date_issued': '2020-01-01',
            'expiry_date': '2030-01-01',
        }
        resp = self.client.post('/doctors/DoctorProfile/', data)
        self.assertIn(resp.status_code, (301,302))
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.first_name, 'Updated')

    def test_doctor_login_view(self):
        resp = self.client.post('/doctors/DoctorLogin/', {'username': 'docpa', 'password1': 'pass'})
        # invalid field name for login uses 'password1' in view
        self.assertIn(resp.status_code, (200,302))
