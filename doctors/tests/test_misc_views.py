from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor, Post


class MiscDoctorViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='docm2', password='pass')
        self.doc = Doctor.objects.create(user=self.user, first_name='MDoc', verification_status='approved')
        from django.core.files.base import ContentFile
        self.doc.photo.save('p.jpg', ContentFile(b''), save=True)

    def test_my_posts_view(self):
        Post.objects.create(author=self.doc, title='X', description='D', content='C')
        self.client.login(username='docm2', password='pass')
        resp = self.client.get('/doctors/Posts/MyPosts')
        self.assertEqual(resp.status_code, 200)

    def test_doctor_logout_redirect(self):
        self.client.login(username='docm2', password='pass')
        resp = self.client.get('/doctors/DoctorLogout/')
        self.assertIn(resp.status_code, (301,302))

    def test_register_doctor_invalid(self):
        # missing password2 triggers invalid branch
        resp = self.client.post('/doctors/DoctorSignUp/', {'username': 'bad', 'email': 'b@b.com', 'password1': 'short'})
        self.assertEqual(resp.status_code, 200)
