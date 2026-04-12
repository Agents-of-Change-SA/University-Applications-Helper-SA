from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from careers.models import CareerAspiration, CareerGuidanceEntry

User = get_user_model()


class CareerAspirationModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='t', password='p')
        asp = CareerAspiration.objects.create(
            user=user, aspiration='Software Engineer',
        )
        self.assertEqual(str(asp), 'Software Engineer')


class CareerAspirationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='t', password='p')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.list_url = '/api/career-aspirations/'

    def test_list_empty(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_create(self):
        resp = self.client.post(
            self.list_url,
            {'aspiration': 'Doctor'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['aspiration'], 'Doctor')

    def test_list_after_create(self):
        CareerAspiration.objects.create(
            user=self.user, aspiration='Lawyer',
        )
        resp = self.client.get(self.list_url)
        self.assertEqual(len(resp.data), 1)

    def test_update(self):
        asp = CareerAspiration.objects.create(
            user=self.user, aspiration='Old',
        )
        resp = self.client.put(
            f'{self.list_url}{asp.pk}/',
            {'aspiration': 'New'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['aspiration'], 'New')

    def test_update_404(self):
        resp = self.client.put(
            f'{self.list_url}99999/',
            {'aspiration': 'X'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        asp = CareerAspiration.objects.create(
            user=self.user, aspiration='Delete Me',
        )
        resp = self.client.delete(f'{self.list_url}{asp.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CareerAspiration.objects.filter(pk=asp.pk).exists())

    def test_delete_404(self):
        resp = self.client.delete(f'{self.list_url}99999/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_isolation_between_users(self):
        other = User.objects.create_user(username='other', password='p')
        CareerAspiration.objects.create(user=other, aspiration='Hidden')
        resp = self.client.get(self.list_url)
        self.assertEqual(len(resp.data), 0)


class CareerGuidanceViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='t', password='p')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.url = '/api/career-guidance/'
        CareerGuidanceEntry.objects.create(
            aspiration='Software Engineer',
            subject='Mathematics',
            explanation='Core requirement',
        )
        CareerGuidanceEntry.objects.create(
            aspiration='Software Engineer',
            subject='IT',
            explanation='Programming',
        )

    def test_get_with_aspiration(self):
        resp = self.client.get(self.url, {'aspiration': 'Software Engineer'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['aspiration'], 'Software Engineer')
        self.assertEqual(len(resp.data['recommendations']), 2)

    def test_get_case_insensitive(self):
        resp = self.client.get(self.url, {'aspiration': 'software engineer'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['recommendations']), 2)

    def test_get_unknown_aspiration(self):
        resp = self.client.get(self.url, {'aspiration': 'Astronaut'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['recommendations'], [])

    def test_get_missing_param(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
