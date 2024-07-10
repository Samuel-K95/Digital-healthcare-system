from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor, Post
from patients.models import Patient
from django.core.files.base import ContentFile
from unittest.mock import patch
import datetime


class DoctorsViewCoverageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doc_user = User.objects.create_user(username='docov', password='pass', email='docov@example.com')
        self.doctor = Doctor.objects.create(
            user=self.doc_user,
            first_name='Doc',
            last_name='Cov',
            verification_status='approved',
            city='Addis',
            region='Oromia',
            country='Ethiopia',
            years_of_experience='3-5',
            languages='English',
            rating=4,
        )
        self.doctor.photo.save('d.jpg', ContentFile(b'x'), save=True)
        self.pat_user = User.objects.create_user(username='patov', password='pass')
        self.patient = Patient.objects.create(user=self.pat_user, fname='P', lname='O', email='po@example.com')

    def test_doctor_login_success_and_failure(self):
        resp_ok = self.client.post('/doctors/DoctorLogin/', {'username': 'docov', 'password1': 'pass'})
        self.assertEqual(resp_ok.status_code, 302)
        self.client.logout()
        resp_bad = self.client.post('/doctors/DoctorLogin/', {'username': 'docov', 'password1': 'wrong'})
        self.assertEqual(resp_bad.status_code, 302)

    def test_doctor_login_get(self):
        self.assertEqual(self.client.get('/doctors/DoctorLogin/').status_code, 200)

    def test_register_doctor_invalid_form(self):
        resp = self.client.post('/doctors/DoctorSignUp/', {
            'username': 'newdoc',
            'email': 'bad',
            'password1': 'short',
            'password2': 'short',
        })
        self.assertEqual(resp.status_code, 200)

    @patch('doctors.views.send_verification_email')
    def test_register_doctor_success(self, mock_send):
        resp = self.client.post('/doctors/DoctorSignUp/', {
            'username': 'newdoc2',
            'email': 'newdoc2@example.com',
            'password1': 'strongpass1',
            'password2': 'strongpass1',
        })
        self.assertEqual(resp.status_code, 302)
        mock_send.assert_called_once()

    def test_doctor_profile_invalid_post(self):
        self.client.login(username='docov', password='pass')
        resp = self.client.post('/doctors/DoctorProfile/', {'first_name': ''})
        self.assertIn(resp.status_code, (200, 302))

    def test_browse_as_doctor_and_patient(self):
        self.client.login(username='docov', password='pass')
        self.assertEqual(self.client.get('/doctors/BrowseDoctors/').status_code, 200)
        self.client.login(username='patov', password='pass')
        self.assertEqual(self.client.get('/doctors/BrowseDoctors/').status_code, 200)

    def test_browse_extended_filters(self):
        base = '/doctors/BrowseDoctors/'
        params = {
            'region': 'Oromia',
            'country': 'Ethiopia',
            'years_of_experience': '3-5',
            'languages': 'English',
            'rating': '3',
        }
        self.assertEqual(self.client.get(base, params).status_code, 200)

    def test_activate_account_invalid(self):
        resp = self.client.get('/doctors/activate/bad/token/')
        self.assertEqual(resp.status_code, 302)

    def test_edit_post_get_and_post(self):
        post = Post.objects.create(
            author=self.doctor,
            title='T',
            description='D',
            content='C',
            published_date=datetime.datetime.now(),
        )
        self.client.login(username='docov', password='pass')
        self.assertEqual(
            self.client.get(f'/doctors/Posts/EditPost/{post.id}/').status_code, 200
        )
        resp = self.client.post(
            f'/doctors/Posts/EditPost/{post.id}/',
            {'title': 'Updated', 'description': 'D2', 'content': 'C2'},
        )
        self.assertIn(resp.status_code, (200, 302))

    def test_doctor_logout(self):
        self.client.login(username='docov', password='pass')
        self.assertEqual(self.client.get('/doctors/DoctorLogout/').status_code, 302)
