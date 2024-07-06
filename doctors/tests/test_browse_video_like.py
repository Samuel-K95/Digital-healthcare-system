from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor, Post
from rating.models import Rating


class BrowseVideoLikeTests(TestCase):
    def setUp(self):
        self.client = Client()
        u1 = User.objects.create_user(username='d1', password='pass')
        u2 = User.objects.create_user(username='d2', password='pass')
        self.doc1 = Doctor.objects.create(user=u1, first_name='Alice', last_name='A', verification_status='approved', city='C1', years_of_experience='1-3', languages='Eng', doctor_type='GP', rating=4.5)
        self.doc2 = Doctor.objects.create(user=u2, first_name='Bob', last_name='B', verification_status='approved', city='C2', years_of_experience='3-5', languages='Spa', doctor_type='Spec', rating=3.0)
        from django.core.files.base import ContentFile
        self.doc1.photo.save('d1.jpg', ContentFile(b''), save=True)
        self.doc2.photo.save('d2.jpg', ContentFile(b''), save=True)
        self.post = Post.objects.create(author=self.doc1, title='P', description='D', content='C')

    def test_browse_filters(self):
        base = '/doctors/BrowseDoctors/'
        res = self.client.get(base)
        self.assertEqual(res.status_code, 200)
        # filter by city
        res2 = self.client.get(base, {'city': 'C1'})
        self.assertEqual(res2.status_code, 200)
        # filter by query
        res3 = self.client.get(base, {'query': 'Alice'})
        self.assertEqual(res3.status_code, 200)

    def test_post_detail_like(self):
        user = User.objects.create_user(username='uguest', password='pass')
        self.client.login(username='uguest', password='pass')
        # first like
        resp = self.client.post(f'/doctors/Posts/PostDetail/{self.post.id}/', {})
        self.assertIn(resp.status_code, (200,302))
        # liking again should trigger error message branch
        resp2 = self.client.post(f'/doctors/Posts/PostDetail/{self.post.id}/', {})
        self.assertIn(resp2.status_code, (200,302))

    def test_start_video_call_branches(self):
        # as doctor
        self.client.login(username='d1', password='pass')
        resp = self.client.get(f'/appointments/VideoCall/1/')
        self.assertIn(resp.status_code, (200,302))
        # as anonymous treated as patient branch
        self.client.logout()
        resp2 = self.client.get(f'/appointments/VideoCall/1/')
        self.assertIn(resp2.status_code, (200,302))
