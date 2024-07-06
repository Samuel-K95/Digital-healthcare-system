from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor, Post


class PostsCrudTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='docp', password='pass')
        self.doctor = Doctor.objects.create(user=self.user, first_name='DocP', verification_status='approved')
        from django.core.files.base import ContentFile
        self.doctor.photo.save('pp.jpg', ContentFile(b''), save=True)

    def login(self):
        self.client.login(username='docp', password='pass')

    def test_create_post(self):
        self.login()
        data = {'title': 'New Post', 'description': 'Desc', 'content': 'Body'}
        resp = self.client.post('/doctors/Posts/CreatePost/', data)
        # should redirect to post_detail
        self.assertIn(resp.status_code, (301,302))
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_edit_and_delete_post(self):
        post = Post.objects.create(author=self.doctor, title='T', description='D', content='C')
        self.login()
        edit_data = {'title': 'T2', 'description': 'D2', 'content': 'C2'}
        resp = self.client.post(f'/doctors/Posts/EditPost/{post.id}/', edit_data)
        self.assertIn(resp.status_code, (301,302))
        post.refresh_from_db()
        self.assertEqual(post.title, 'T2')

        resp2 = self.client.get(f'/doctors/Posts/DeletePost/{post.id}/')
        self.assertIn(resp2.status_code, (301,302))
        self.assertFalse(Post.objects.filter(id=post.id).exists())
