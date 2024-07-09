from django.test import TestCase, Client
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
import datetime


class AppointmentsViewCoverageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.doc_user = User.objects.create_user(username='docvc', password='pass')
        self.pat_user = User.objects.create_user(username='patvc', password='pass')
        self.doctor = Doctor.objects.create(user=self.doc_user, first_name='Doc', last_name='VC')
        from django.core.files.base import ContentFile
        self.doctor.photo.save('docvc.jpg', ContentFile(b'x'), save=True)
        self.patient = Patient.objects.create(user=self.pat_user, fname='Pat', lname='VC', email='pvc@example.com')
        self.appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=datetime.datetime.now() + datetime.timedelta(days=3),
        )

    def test_schedule_requires_login(self):
        resp = self.client.get(f'/appointments/schedule_appointment/{self.doctor.id}/')
        self.assertEqual(resp.status_code, 302)

    def test_schedule_invalid_form_shows_errors(self):
        self.client.login(username='patvc', password='pass')
        resp = self.client.post(
            f'/appointments/schedule_appointment/{self.doctor.id}/',
            {'appointment_date': '', 'additional_requests': ''},
        )
        self.assertEqual(resp.status_code, 200)

    def test_view_appointment_lists(self):
        self.client.login(username='docvc', password='pass')
        resp_doc = self.client.get('/appointments/view_patient_appointments/')
        self.assertEqual(resp_doc.status_code, 200)
        self.client.login(username='patvc', password='pass')
        resp_pat = self.client.get('/appointments/view_doctor_appointments/')
        self.assertEqual(resp_pat.status_code, 200)

    def test_reschedule_and_edit_invalid_forms(self):
        self.client.login(username='docvc', password='pass')
        bad_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        resp_res = self.client.post(
            f'/appointments/reschedule_appointment/{self.appt.id}/',
            {'appointment_date': bad_date},
        )
        self.assertIn(resp_res.status_code, (200, 302))
        resp_edit = self.client.post(
            f'/appointments/edit_appointment/{self.appt.id}/',
            {'appointment_date': bad_date, 'additional_requests': 'x'},
        )
        self.assertIn(resp_edit.status_code, (200, 302))

    def test_reschedule_and_edit_get_forms(self):
        self.client.login(username='docvc', password='pass')
        self.assertEqual(
            self.client.get(f'/appointments/reschedule_appointment/{self.appt.id}/').status_code, 200
        )
        self.assertEqual(
            self.client.get(f'/appointments/edit_appointment/{self.appt.id}/').status_code, 200
        )

    def test_join_the_call_redirects(self):
        self.client.login(username='patvc', password='pass')
        resp = self.client.get(f'/appointments/join_the_call/{self.appt.id}')
        self.assertEqual(resp.status_code, 302)

    def test_video_call_as_patient(self):
        self.client.login(username='patvc', password='pass')
        resp = self.client.get(f'/appointments/VideoCall/{self.appt.id}/')
        self.assertEqual(resp.status_code, 200)
