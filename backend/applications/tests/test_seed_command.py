from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from applications.models import ApplicationEntry


class SeedApplicationDatesTest(TestCase):
    def test_creates_7_entries(self):
        out = StringIO()
        call_command('seed_application_dates', stdout=out)
        self.assertEqual(ApplicationEntry.objects.count(), 7)

    def test_idempotent(self):
        call_command('seed_application_dates', stdout=StringIO())
        call_command('seed_application_dates', stdout=StringIO())
        self.assertEqual(ApplicationEntry.objects.count(), 7)

    def test_institution_names(self):
        call_command('seed_application_dates', stdout=StringIO())
        names = set(
            ApplicationEntry.objects.values_list('institution_name', flat=True),
        )
        expected = {
            'University of Cape Town',
            'University of the Witwatersrand',
            'Stellenbosch University',
            'University of Pretoria',
            'University of KwaZulu-Natal',
            'Durban University of Technology',
            'University of Johannesburg',
        }
        self.assertEqual(names, expected)

    def test_fee_range(self):
        call_command('seed_application_dates', stdout=StringIO())
        fees = list(
            ApplicationEntry.objects.values_list('application_fee', flat=True),
        )
        self.assertTrue(min(fees) >= 0)
        self.assertTrue(max(fees) <= 300)

    def test_output_messages(self):
        out = StringIO()
        call_command('seed_application_dates', stdout=out)
        output = out.getvalue()
        self.assertIn('Created', output)
