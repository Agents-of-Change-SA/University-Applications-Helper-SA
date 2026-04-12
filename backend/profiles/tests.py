from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from profiles.models import UserDetails

User = get_user_model()


class UserDetailsModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='t', password='p')
        details = UserDetails.objects.create(
            user=user, name='Thandi', surname='Mkhize', age=17,
        )
        self.assertEqual(str(details), 'Thandi Mkhize')


class UserDetailsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/user-details/'
        self.user = User.objects.create_user(username='t', password='p')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_404_when_no_details(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_creates_details(self):
        data = {'name': 'Thandi', 'surname': 'Mkhize', 'age': 17}
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], 'Thandi')

    def test_get_after_create(self):
        UserDetails.objects.create(
            user=self.user, name='Thandi', surname='Mkhize', age=17,
        )
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['surname'], 'Mkhize')

    def test_patch_updates(self):
        UserDetails.objects.create(
            user=self.user, name='Thandi', surname='Mkhize', age=17,
        )
        resp = self.client.patch(self.url, {'age': 18}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['age'], 18)

    def test_unauthenticated(self):
        self.client.credentials()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
