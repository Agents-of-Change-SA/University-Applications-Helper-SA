from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tutors.models import Tutor

User = get_user_model()


class TutorModelTest(TestCase):
    def test_str(self):
        t = Tutor(name='Thabo', subject='Mathematics')
        self.assertEqual(str(t), 'Thabo (Mathematics)')


class TutorViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='t', password='p')
        cls.token = Token.objects.create(user=cls.user)
        Tutor.objects.create(
            name='Thabo Mokoena', subject='Mathematics', contact='+27 XX',
        )
        Tutor.objects.create(
            name='Naledi Dlamini', subject='Physical Sciences', contact='+27 XX',
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.url = '/api/tutors/'

    def test_list(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_filter_by_subject(self):
        resp = self.client.get(self.url, {'subject': 'math'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], 'Thabo Mokoena')

    def test_search_by_name(self):
        resp = self.client.get(self.url, {'search': 'Naledi'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_response_shape(self):
        resp = self.client.get(self.url)
        first = resp.data[0]
        self.assertIn('id', first)
        self.assertIn('name', first)
        self.assertIn('subject', first)
        self.assertIn('contact', first)

    def test_retrieve(self):
        tutor = Tutor.objects.first()
        resp = self.client.get(f'{self.url}{tutor.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], tutor.name)
