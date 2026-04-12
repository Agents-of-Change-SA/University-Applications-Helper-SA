from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/accounts/register/'

    def test_register_success(self):
        data = {
            'username': 'thandi',
            'first_name': 'Thandi',
            'last_name': 'Mkhize',
            'email': 'thandi@example.com',
            'password': 'Str0ng!Pass',
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='thandi').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user(
            username='existing', email='dup@example.com', password='x',
        )
        data = {
            'username': 'new',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'dup@example.com',
            'password': 'Str0ng!Pass',
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', resp.data)

    def test_register_weak_password(self):
        data = {
            'username': 'weak',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'weak@example.com',
            'password': 'short',
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', resp.data)

    def test_register_short_first_name(self):
        data = {
            'username': 'short',
            'first_name': 'A',
            'last_name': 'User',
            'email': 'short@example.com',
            'password': 'Str0ng!Pass',
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', resp.data)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/accounts/login/'
        self.user = User.objects.create_user(
            username='thandi', password='Str0ng!Pass', email='t@example.com',
            first_name='Thandi', last_name='Mkhize',
        )

    def test_login_success(self):
        resp = self.client.post(
            self.url, {'username': 'thandi', 'password': 'Str0ng!Pass'}, format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)
        self.assertEqual(resp.data['username'], 'thandi')
        self.assertEqual(resp.data['first_name'], 'Thandi')

    def test_login_invalid_credentials(self):
        resp = self.client.post(
            self.url, {'username': 'thandi', 'password': 'wrong'}, format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/accounts/logout/'
        self.user = User.objects.create_user(username='u', password='p')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_logout_success(self):
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated(self):
        self.client.credentials()
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/accounts/profile/'
        self.user = User.objects.create_user(
            username='thandi', password='p', email='t@e.com',
            first_name='Thandi', last_name='Mkhize',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_profile_success(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['username'], 'thandi')

    def test_profile_unauthenticated(self):
        self.client.credentials()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
