from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from applications.models import ApplicationEntry


class ApplicationEntryModelTest(TestCase):
    def _make_entry(self, **kwargs):
        defaults = {
            'institution_name': 'University of Cape Town',
            'open_date': date(2026, 3, 1),
            'close_date': date(2026, 6, 30),
            'application_fee': Decimal('100.00'),
            'portal_url': 'https://uct.ac.za/apply',
        }
        defaults.update(kwargs)
        return ApplicationEntry(**defaults)

    def test_str(self):
        entry = self._make_entry()
        self.assertEqual(str(entry), 'University of Cape Town')

    def test_meta_ordering(self):
        self.assertEqual(
            ApplicationEntry._meta.ordering, ['institution_name'],
        )

    def test_meta_verbose_name(self):
        self.assertEqual(
            ApplicationEntry._meta.verbose_name, 'Application Entry',
        )
        self.assertEqual(
            ApplicationEntry._meta.verbose_name_plural, 'Application Entries',
        )

    def test_clean_valid_dates(self):
        entry = self._make_entry()
        entry.full_clean()  # should not raise

    def test_clean_equal_dates(self):
        entry = self._make_entry(
            open_date=date(2026, 5, 1),
            close_date=date(2026, 5, 1),
        )
        entry.full_clean()  # should not raise

    def test_clean_invalid_dates(self):
        entry = self._make_entry(
            open_date=date(2026, 9, 1),
            close_date=date(2026, 3, 1),
        )
        with self.assertRaises(ValidationError) as ctx:
            entry.full_clean()
        self.assertIn('close_date', ctx.exception.message_dict)

    def test_save_enforces_validation(self):
        entry = self._make_entry(
            open_date=date(2026, 9, 1),
            close_date=date(2026, 3, 1),
        )
        with self.assertRaises(ValidationError):
            entry.save()

    def test_save_valid(self):
        entry = self._make_entry()
        entry.save()
        self.assertIsNotNone(entry.pk)
        self.assertEqual(ApplicationEntry.objects.count(), 1)

    def test_field_types(self):
        opts = ApplicationEntry._meta
        self.assertEqual(opts.get_field('institution_name').max_length, 255)
        self.assertEqual(opts.get_field('application_fee').max_digits, 10)
        self.assertEqual(opts.get_field('application_fee').decimal_places, 2)
        self.assertEqual(opts.get_field('portal_url').max_length, 500)
