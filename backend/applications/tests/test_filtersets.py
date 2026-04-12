from datetime import date
from decimal import Decimal

from django.test import TestCase

from applications.filtersets import ApplicationEntryFilterSet
from applications.models import ApplicationEntry


class ApplicationEntryFilterSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.uct = ApplicationEntry.objects.create(
            institution_name='University of Cape Town',
            open_date=date(2026, 3, 1),
            close_date=date(2026, 6, 30),
            application_fee=Decimal('100.00'),
            portal_url='https://uct.ac.za',
        )
        cls.wits = ApplicationEntry.objects.create(
            institution_name='University of the Witwatersrand',
            open_date=date(2026, 4, 1),
            close_date=date(2026, 9, 30),
            application_fee=Decimal('200.00'),
            portal_url='https://wits.ac.za',
        )
        cls.dut = ApplicationEntry.objects.create(
            institution_name='Durban University of Technology',
            open_date=date(2025, 9, 1),
            close_date=date(2025, 11, 30),
            application_fee=Decimal('0.00'),
            portal_url='https://dut.ac.za',
        )

    def _filter(self, **params):
        qs = ApplicationEntry.objects.all()
        fs = ApplicationEntryFilterSet(data=params, queryset=qs)
        return fs.qs

    def test_institution_name_icontains(self):
        result = self._filter(institution_name='cape')
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().pk, self.uct.pk)

    def test_institution_name_case_insensitive(self):
        result = self._filter(institution_name='DURBAN')
        self.assertEqual(result.count(), 1)

    def test_open_date_from(self):
        result = self._filter(open_date_from='2026-04-01')
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().pk, self.wits.pk)

    def test_open_date_to(self):
        result = self._filter(open_date_to='2025-09-01')
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().pk, self.dut.pk)

    def test_close_date_range(self):
        result = self._filter(
            close_date_from='2026-06-01', close_date_to='2026-07-01',
        )
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().pk, self.uct.pk)

    def test_min_fee(self):
        result = self._filter(min_fee=100)
        self.assertEqual(result.count(), 2)

    def test_max_fee(self):
        result = self._filter(max_fee=100)
        self.assertEqual(result.count(), 2)  # UCT (100) + DUT (0)

    def test_combined_filters(self):
        result = self._filter(institution_name='university', min_fee=100, max_fee=150)
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().pk, self.uct.pk)

    def test_no_filters_returns_all(self):
        result = self._filter()
        self.assertEqual(result.count(), 3)
