from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from careers.models import CareerGuidanceEntry


class SeedCareerGuidanceTest(TestCase):
    def test_creates_15_entries(self):
        call_command('seed_career_guidance', stdout=StringIO())
        self.assertEqual(CareerGuidanceEntry.objects.count(), 15)

    def test_idempotent(self):
        call_command('seed_career_guidance', stdout=StringIO())
        call_command('seed_career_guidance', stdout=StringIO())
        self.assertEqual(CareerGuidanceEntry.objects.count(), 15)

    def test_covers_5_aspirations(self):
        call_command('seed_career_guidance', stdout=StringIO())
        aspirations = set(
            CareerGuidanceEntry.objects.values_list('aspiration', flat=True),
        )
        self.assertEqual(len(aspirations), 5)
