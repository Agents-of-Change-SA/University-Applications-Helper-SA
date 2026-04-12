from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from qualifications.models import (
    APSRuleCondition,
    Institution,
    Qualification,
    SubjectRequirement,
)


class SeedQualificationsTest(TestCase):
    def test_creates_institutions(self):
        call_command('seed_qualifications', stdout=StringIO())
        self.assertEqual(Institution.objects.count(), 3)

    def test_creates_qualifications(self):
        call_command('seed_qualifications', stdout=StringIO())
        self.assertEqual(Qualification.objects.count(), 3)

    def test_idempotent(self):
        call_command('seed_qualifications', stdout=StringIO())
        call_command('seed_qualifications', stdout=StringIO())
        self.assertEqual(Institution.objects.count(), 3)
        self.assertEqual(Qualification.objects.count(), 3)

    def test_aps_rule_conditions_created(self):
        call_command('seed_qualifications', stdout=StringIO())
        # UJ BA Interior Design has 2 APS rule conditions
        uj_qual = Qualification.objects.get(slug='uj-ba-interior-design')
        conditions = APSRuleCondition.objects.filter(rule__qualification=uj_qual)
        self.assertEqual(conditions.count(), 2)

    def test_subject_requirements_created(self):
        call_command('seed_qualifications', stdout=StringIO())
        uj_qual = Qualification.objects.get(slug='uj-ba-interior-design')
        mandatory = SubjectRequirement.objects.filter(
            qualification=uj_qual, requirement_type='mandatory',
        )
        self.assertEqual(mandatory.count(), 1)
        self.assertEqual(mandatory.first().subject, 'English')

    def test_disallowed_subjects(self):
        call_command('seed_qualifications', stdout=StringIO())
        uj_qual = Qualification.objects.get(slug='uj-ba-interior-design')
        disallowed = SubjectRequirement.objects.filter(
            qualification=uj_qual, requirement_type='disallowed',
        )
        self.assertEqual(disallowed.count(), 1)
        self.assertEqual(disallowed.first().subject, 'Technical Mathematics')
