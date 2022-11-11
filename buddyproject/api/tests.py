from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.serializer import RoomSerializer
import requests
# Create your tests here.

class RoomTest(APITestCase):
    def test_default(self):
        response = self.client.get(reverse('list_routes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], 'GET /api')
        self.assertEqual(response.data[1], 'GET /api/rooms/')
        self.assertEqual(response.data[2], 'GET /api/rooms/:id')


    def test_listRoom(self):
        response = requests.get('http://127.0.0.1:8000/api/rooms/')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0].get('name'), 'Learn Django')
        self.assertEqual(len(data), 3)


    def test_getRoom(self):
        response = requests.get('http://127.0.0.1:8000/api/rooms/', params={'id':'3'})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0].get('name'), 'Learn Django')
