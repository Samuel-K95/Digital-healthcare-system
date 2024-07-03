from django.test import TestCase
from django.contrib.auth.models import User
from doctors.models import Doctor


class DoctorModelTests(TestCase):
    def test_doctor_str(self):
        user = User.objects.create_user(username='docmod', password='pass')
        doc = Doctor.objects.create(user=user, first_name='John', last_name='Doe')
        self.assertIn('John', str(doc))
