from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from .tasks import send_test_email_task


class TestEmailTask(SimpleTestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('acount.tasks.EmailMessage.send')
    def test_send_test_email_task_sends_html_email(self, mock_send):
        send_test_email_task.run('user@example.com', 'Test email', {'task_id': 'abc-123'})

        self.assertTrue(mock_send.called)

    @patch('acount.views.send_test_email_task.delay')
    def test_test_task_view_starts_async_email_task(self, mock_delay):
        mock_delay.return_value.id = 'task-123'

        response = self.client.get(reverse('test_task'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'task-123')
        mock_delay.assert_called_once()
