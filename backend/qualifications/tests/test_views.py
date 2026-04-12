from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from qualifications.models import (
    APSRule,
    APSRuleCondition,
    Institution,
    Qualification,
    SubjectRequirement,
)

User = get_user_model()


class QualificationViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='pass')
        cls.token = Token.objects.create(user=cls.user)
        cls.uj = Institution.objects.create(
            name='University of Johannesburg', abbreviation='UJ',
        )
        cls.uct = Institution.objects.create(
            name='University of Cape Town', abbreviation='UCT',
        )
        cls.qual1 = Qualification.objects.create(
            institution=cls.uj, slug='uj-ba-interior',
            name='BA Interior Design', qualification_code='B8BA6Q',
            faculty='Art', minimum_aps=25,
        )
        cls.qual2 = Qualification.objects.create(
            institution=cls.uct, slug='uct-bsc-cs',
            name='BSc Computer Science', qualification_code='SC016',
            faculty='Science', minimum_aps=34,
        )
        SubjectRequirement.objects.create(
            qualification=cls.qual2, requirement_type='mandatory',
            subject='Mathematics', minimum_level=5,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    # --- Qualification list ---
    def test_list_200(self):
        resp = self.client.get('/api/qualifications/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_list_has_institution_fields(self):
        resp = self.client.get('/api/qualifications/')
        first = resp.data[0]
        self.assertIn('institution_name', first)
        self.assertIn('institution_abbr', first)

    def test_list_filter_by_name(self):
        resp = self.client.get('/api/qualifications/', {'name': 'interior'})
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['slug'], 'uj-ba-interior')

    def test_list_filter_by_institution_name(self):
        resp = self.client.get('/api/qualifications/', {'institution_name': 'cape'})
        self.assertEqual(len(resp.data), 1)

    def test_list_filter_by_min_aps(self):
        resp = self.client.get('/api/qualifications/', {'min_aps': 30})
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['minimum_aps'], 34)

    def test_list_filter_by_max_aps(self):
        resp = self.client.get('/api/qualifications/', {'max_aps': 30})
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['minimum_aps'], 25)

    def test_list_search(self):
        resp = self.client.get('/api/qualifications/', {'search': 'Computer'})
        self.assertEqual(len(resp.data), 1)

    def test_list_ordering(self):
        resp = self.client.get('/api/qualifications/', {'ordering': '-minimum_aps'})
        aps_values = [q['minimum_aps'] for q in resp.data]
        self.assertEqual(aps_values, sorted(aps_values, reverse=True))

    # --- Qualification detail ---
    def test_detail_200(self):
        resp = self.client.get(f'/api/qualifications/{self.qual2.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'BSc Computer Science')
        self.assertIn('subject_requirements', resp.data)
        self.assertIn('aps_rules', resp.data)
        self.assertIn('selection_requirements', resp.data)

    def test_detail_subject_requirements_grouped(self):
        resp = self.client.get(f'/api/qualifications/{self.qual2.pk}/')
        sr = resp.data['subject_requirements']
        self.assertEqual(len(sr['mandatory']), 1)
        self.assertEqual(sr['mandatory'][0]['subject'], 'Mathematics')

    def test_detail_404(self):
        resp = self.client.get('/api/qualifications/99999/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # --- Institution list ---
    def test_institution_list(self):
        resp = self.client.get('/api/institutions/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_institution_filter(self):
        resp = self.client.get('/api/institutions/', {'name': 'johannesburg'})
        self.assertEqual(len(resp.data), 1)

    # --- Institution detail ---
    def test_institution_detail_with_qualifications(self):
        resp = self.client.get(f'/api/institutions/{self.uj.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'University of Johannesburg')
        self.assertEqual(len(resp.data['qualifications']), 1)

    def test_institution_detail_404(self):
        resp = self.client.get('/api/institutions/99999/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
