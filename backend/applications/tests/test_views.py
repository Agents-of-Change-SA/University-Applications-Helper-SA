from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from applications.models import ApplicationEntry

User = get_user_model()


class ApplicationEntryViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='pass')
        cls.token = Token.objects.create(user=cls.user)
        cls.uct = ApplicationEntry.objects.create(
            institution_name='University of Cape Town',
            open_date=date(2026, 3, 1),
            close_date=date(2026, 6, 30),
            application_fee=Decimal('100.00'),
            portal_url='https://uct.ac.za',
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.list_url = '/api/application-dates/'
        self.detail_url = f'/api/application-dates/{self.uct.pk}/'

    # --- LIST ---
    def test_list_200(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 1)

    def test_list_filter_institution_name(self):
        resp = self.client.get(self.list_url, {'institution_name': 'cape'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_list_search(self):
        resp = self.client.get(self.list_url, {'search': 'Cape Town'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_list_ordering(self):
        ApplicationEntry.objects.create(
            institution_name='AAA University',
            open_date=date(2026, 1, 1),
            close_date=date(2026, 12, 31),
            application_fee=Decimal('50.00'),
            portal_url='https://aaa.ac.za',
        )
        resp = self.client.get(self.list_url, {'ordering': 'institution_name'})
        names = [e['institution_name'] for e in resp.data]
        self.assertEqual(names, sorted(names))

    # --- RETRIEVE ---
    def test_retrieve_200(self):
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['institution_name'], 'University of Cape Town')

    def test_retrieve_404(self):
        resp = self.client.get('/api/application-dates/99999/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- CREATE ---
    def test_create_201(self):
        payload = {
            'institution_name': 'New University',
            'open_date': '2026-05-01',
            'close_date': '2026-10-31',
            'application_fee': '150.00',
            'portal_url': 'https://new.ac.za',
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['institution_name'], 'New University')

    def test_create_400_missing_fields(self):
        resp = self.client.post(self.list_url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('institution_name', resp.data)
        self.assertIn('open_date', resp.data)

    def test_create_400_bad_dates(self):
        payload = {
            'institution_name': 'Bad Dates',
            'open_date': '2026-09-01',
            'close_date': '2026-03-01',
            'application_fee': '100.00',
            'portal_url': 'https://bad.ac.za',
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('close_date', resp.data)

    # --- UPDATE ---
    def test_put_200(self):
        payload = {
            'institution_name': 'UCT Updated',
            'open_date': '2026-03-01',
            'close_date': '2026-07-31',
            'application_fee': '120.00',
            'portal_url': 'https://uct.ac.za/apply',
        }
        resp = self.client.put(self.detail_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['institution_name'], 'UCT Updated')

    def test_patch_200(self):
        resp = self.client.patch(
            self.detail_url,
            {'application_fee': '999.00'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['application_fee'], '999.00')

    # --- DELETE ---
    def test_delete_204(self):
        entry = ApplicationEntry.objects.create(
            institution_name='To Delete',
            open_date=date(2026, 1, 1),
            close_date=date(2026, 12, 31),
            application_fee=Decimal('0'),
            portal_url='https://del.ac.za',
        )
        resp = self.client.delete(f'/api/application-dates/{entry.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ApplicationEntry.objects.filter(pk=entry.pk).exists())

    def test_delete_404(self):
        resp = self.client.delete('/api/application-dates/99999/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
