from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor, Post


class DoctorsViewsBasicTests(TestCase):
    def setUp(self):
        self.client = Client()
        # create two users and doctors
        u1 = User.objects.create_user(username='doc1', password='pass')
        u2 = User.objects.create_user(username='doc2', password='pass')
        self.doc1 = Doctor.objects.create(user=u1, first_name='Alice', last_name='One', verification_status='approved', city='X')
        self.doc2 = Doctor.objects.create(user=u2, first_name='Bob', last_name='Two', verification_status='approved', city='Y')
        # ensure photo fields have a file to avoid template .url errors
        from django.core.files.base import ContentFile
        self.doc1.photo.save('p1.jpg', ContentFile(b''), save=True)
        self.doc2.photo.save('p2.jpg', ContentFile(b''), save=True)

        # create posts
        Post.objects.create(author=self.doc1, title='T1', description='D', content='C')

    def test_browse_doctors_anonymous(self):
        resp = self.client.get('/doctors/BrowseDoctors/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('doctors', resp.context)

    def test_post_list_and_detail(self):
        resp = self.client.get('/doctors/Posts/')
        self.assertEqual(resp.status_code, 200)
        posts = resp.context.get('posts')
        self.assertTrue(posts.exists())

        post = posts.first()
        resp2 = self.client.get(f'/doctors/Posts/PostDetail/{post.id}/')
        self.assertEqual(resp2.status_code, 200)
