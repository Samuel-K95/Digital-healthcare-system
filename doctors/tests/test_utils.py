from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock

from doctors import utils


class UtilsEmailTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.user = User.objects.create_user(username='mailuser', email='u@example.com', password='pass')

    @patch('doctors.utils.render_to_string')
    @patch('doctors.utils.get_current_site')
    @patch('doctors.utils.EmailMessage')
    def test_send_verification_email_calls_email(self, mock_email_cls, mock_get_site, mock_render):
        mock_get_site.return_value = 'example.com'
        mock_render.return_value = 'welcome'
        mock_mail = MagicMock()
        mock_email_cls.return_value = mock_mail

        utils.send_verification_email(self.request, self.user, 'subj', 'template.html')

        mock_render.assert_called()
        mock_email_cls.assert_called()
        mock_mail.send.assert_called_once()

    @patch('doctors.utils.render_to_string')
    @patch('doctors.utils.EmailMessage')
    def test_send_notification_calls_email(self, mock_email_cls, mock_render):
        mock_render.return_value = 'notify'
        mock_mail = MagicMock()
        mock_email_cls.return_value = mock_mail
        ctx = {'user': self.user}

        utils.send_notification('subj', 'template.html', ctx)

        mock_render.assert_called()
        mock_email_cls.assert_called()
        mock_mail.send.assert_called_once()
