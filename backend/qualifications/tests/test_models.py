from django.test import TestCase

from qualifications.models import (
    APSRule,
    APSRuleCondition,
    Institution,
    Qualification,
    SelectionRequirement,
    SubjectRequirement,
)


class InstitutionModelTest(TestCase):
    def test_str_with_abbreviation(self):
        inst = Institution(name='University of Johannesburg', abbreviation='UJ')
        self.assertEqual(str(inst), 'UJ')

    def test_str_without_abbreviation(self):
        inst = Institution(name='University of Johannesburg', abbreviation='')
        self.assertEqual(str(inst), 'University of Johannesburg')

    def test_ordering(self):
        self.assertEqual(Institution._meta.ordering, ['name'])


class QualificationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inst = Institution.objects.create(name='UJ', abbreviation='UJ')

    def test_str(self):
        q = Qualification(name='BA Interior Design', institution=self.inst)
        self.assertEqual(str(q), 'BA Interior Design (UJ)')

    def test_ordering(self):
        self.assertEqual(Qualification._meta.ordering, ['institution', 'name'])


class SubjectRequirementModelTest(TestCase):
    def test_str(self):
        sr = SubjectRequirement(
            requirement_type='mandatory', subject='English', minimum_level=5,
        )
        self.assertEqual(str(sr), 'mandatory: English (level 5)')


class APSRuleConditionModelTest(TestCase):
    def test_str(self):
        c = APSRuleCondition(subject='Mathematics', minimum_level=4, min_aps=25)
        self.assertEqual(str(c), 'Mathematics level 4 → APS 25')


class SelectionRequirementModelTest(TestCase):
    def test_str_required(self):
        sr = SelectionRequirement(selection_type='nbt', required=True)
        self.assertEqual(str(sr), 'nbt (required)')

    def test_str_optional(self):
        sr = SelectionRequirement(selection_type='possible_portfolio', required=False)
        self.assertEqual(str(sr), 'possible_portfolio (optional)')
