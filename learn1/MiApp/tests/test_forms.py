from django.test import TestCase
from django.core import mail
from MiApp.forms import ContactForm

# Create your tests here.
class TestForm(TestCase):
    def test_valid_contact_us_form_sends_email(self):
        form=ContactForm({'name':"Luke Skywalker", 'message':"thanks for the cool website"})
        self.assertTrue(form.is_valid())
        with self.assertLogs('MiApp.forms', level='INFO') as cm:form.send_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Site message')
        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_contact_us_form(self):
        form=ContactForm({'message':"thanks for the cool website"})
        self.assertFalse(form.is_valid())
