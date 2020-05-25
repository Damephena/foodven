import json

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

from users.models import Auth, Customer, Vendor
from services.models import Report, Order, Menu, Notification
from services.serializers import MenuSerializer, OrderSerializer
# Create your tests here.

client = Client()
factory = APIRequestFactory()

class MenuTest(TestCase):
    '''Test module for Menu model.'''
    def setUp(self):
        self.ven = Auth.objects.create(email='ven1@gmail.com', password='1234pass')
        self.vendor1 = Vendor.objects.create(first_name='ven', last_name='a', email='ven1@gmail.com', business_name='ven-a')
        self.vendor2 = Vendor.objects.create(first_name='b', last_name='b', email='ven2@gmail.com', business_name='ven-b')
        
        token = Token.objects.get(vendor__email='ven1@gmail.com')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.menu1 = Menu.objects.create(vendor=self.vendor1, name='menu 1', description='fine menu', price=350, quantity=54, is_recurring=False)
        self.menu2 = Menu.objects.create(vendor=self.vendor1, name='menu 2', price=200, quantity=2, is_recurring=True)
        self.menu3 = Menu.objects.create(vendor=self.vendor2, name='menu 3', price=500, quantity=20, is_recurring=True)

        # test for insertion
        self.valid_payload = {
            'vendor':self.vendor1.id,
            'name' : 'Yam and egg sauce',
            'description': 'Carrot and plantain is available',
            'price': 300,
            'quantity': 4,
            'is_recurring': True
        }

        self.invalid_payload = {
            'vendor': self.vendor1.id,
            'name' : '',
            'description': 'Carrot and plantain is available',
            'price': 300,
            'quantity': 4,
            'is_recurring': True
        }

    def test_get_all_menus(self):
        response = client.get(reverse('menu-list'))
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_menu(self):
        response = client.get(
            reverse('menu-detail', kwargs={'pk': self.menu1.pk})
        )
        menu = Menu.objects.get(pk=self.menu1.pk)
        serializer = MenuSerializer(menu, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_menu(self):
        response = client.get(
            reverse('menu-detail', kwargs={'pk': 100})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menu(self):
        response = client.post(
            reverse('menu-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    