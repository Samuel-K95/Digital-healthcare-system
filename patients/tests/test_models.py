from django.test import TestCase
from django.contrib.auth.models import User
from patients.models import Patient
import datetime


class PatientModelTests(TestCase):
    def test_age_calculation_on_save(self):
        user = User.objects.create_user(username='patmod', password='pass')
        dob = datetime.date.today() - datetime.timedelta(days=365*30)
        p = Patient.objects.create(user=user, fname='Alice', lname='Smith', email='a@example.com', date_of_birth=dob)
        self.assertTrue(p.age >= 29)
