from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from tutors.models import Tutor


class SeedTutorsTest(TestCase):
    def test_creates_6_tutors(self):
        call_command('seed_tutors', stdout=StringIO())
        self.assertEqual(Tutor.objects.count(), 6)

    def test_idempotent(self):
        call_command('seed_tutors', stdout=StringIO())
        call_command('seed_tutors', stdout=StringIO())
        self.assertEqual(Tutor.objects.count(), 6)
