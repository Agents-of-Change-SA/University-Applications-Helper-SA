from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from school.models import SchoolProfile, SchoolSubject

User = get_user_model()


class SchoolProfileModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='t', password='p')
        profile = SchoolProfile.objects.create(
            user=user, school_name='Pretoria High',
        )
        self.assertEqual(str(profile), 'Pretoria High')


class SchoolProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/school-profile/'
        self.user = User.objects.create_user(username='t', password='p')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_404_when_no_profile(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_creates_profile(self):
        data = {
            'name': 'Pretoria High',
            'subjects': [
                {'name': 'Mathematics', 'percentage': 78, 'level': 7},
                {'name': 'English', 'percentage': 72, 'level': 6},
            ],
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['school_name'], 'Pretoria High')
        self.assertEqual(len(resp.data['subjects']), 2)

    def test_post_updates_existing(self):
        profile = SchoolProfile.objects.create(
            user=self.user, school_name='Old School',
        )
        SchoolSubject.objects.create(
            profile=profile, name='Math', percentage=50, level=4,
        )
        data = {
            'name': 'New School',
            'subjects': [
                {'name': 'English', 'percentage': 80, 'level': 7},
            ],
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['school_name'], 'New School')
        self.assertEqual(len(resp.data['subjects']), 1)
