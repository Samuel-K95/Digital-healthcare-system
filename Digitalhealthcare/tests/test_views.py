from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor, Post
from django.utils import timezone


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_renders(self):
        # ensure view renders without posts
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_home_with_posts(self):
        user = User.objects.create_user(username='postuser', password='pass')
        doc = Doctor.objects.create(user=user)
        Post.objects.create(author=doc, title='T', description='D', content='C', published_date=timezone.now())
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'T')
