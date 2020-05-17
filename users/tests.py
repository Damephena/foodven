from django.core import mail
from django.test import TestCase

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token

from users.models import Auth, Customer, Vendor
# from users import 

class TestCustomer(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

        @staticmethod
        def setup_user():
            User = Customer.objects.all()
            return Customer.objects.create_user(
                'testuser@gmail.com',
                'test123',
                first_name='test'
            )

class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            'That’s your subject', 'That’s your message body',
            'from@yourdjangoapp.com', ['to@yourbestuser.com'],
            fail_silently=False,
        )

        self.assertEqual(len(mail.outbox), 1)        
        self.assertEqual(mail.outbox[0].subject, 'That’s your subject')
        self.assertEqual(mail.outbox[0].body, 'That’s your message body')
        