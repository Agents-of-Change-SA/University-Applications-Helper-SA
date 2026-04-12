from datetime import date
from decimal import Decimal

from django.test import TestCase

from applications.models import ApplicationEntry
from applications.serializers import ApplicationEntrySerializer


class ApplicationEntrySerializerTest(TestCase):
    def _make_entry(self):
        return ApplicationEntry.objects.create(
            institution_name='UCT',
            open_date=date(2026, 3, 1),
            close_date=date(2026, 6, 30),
            application_fee=Decimal('100.00'),
            portal_url='https://uct.ac.za/apply',
        )

    def test_fields(self):
        expected = {'id', 'institution_name', 'open_date', 'close_date',
                    'application_fee', 'portal_url'}
        entry = self._make_entry()
        data = ApplicationEntrySerializer(entry).data
        self.assertEqual(set(data.keys()), expected)

    def test_date_format(self):
        entry = self._make_entry()
        data = ApplicationEntrySerializer(entry).data
        self.assertEqual(data['open_date'], '2026-03-01')
        self.assertEqual(data['close_date'], '2026-06-30')

    def test_fee_is_string(self):
        entry = self._make_entry()
        data = ApplicationEntrySerializer(entry).data
        self.assertIsInstance(data['application_fee'], str)
        self.assertEqual(data['application_fee'], '100.00')

    def test_validate_rejects_bad_dates(self):
        payload = {
            'institution_name': 'Test',
            'open_date': '2026-09-01',
            'close_date': '2026-03-01',
            'application_fee': '100.00',
            'portal_url': 'https://example.com',
        }
        s = ApplicationEntrySerializer(data=payload)
        self.assertFalse(s.is_valid())
        self.assertIn('close_date', s.errors)

    def test_validate_accepts_good_dates(self):
        payload = {
            'institution_name': 'Test',
            'open_date': '2026-03-01',
            'close_date': '2026-06-30',
            'application_fee': '100.00',
            'portal_url': 'https://example.com',
        }
        s = ApplicationEntrySerializer(data=payload)
        self.assertTrue(s.is_valid(), s.errors)
