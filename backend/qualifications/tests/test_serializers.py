from django.test import TestCase

from qualifications.models import (
    APSRule,
    APSRuleCondition,
    Institution,
    Qualification,
    SelectionRequirement,
    SubjectRequirement,
)
from qualifications.serializers import (
    InstitutionDetailSerializer,
    InstitutionSerializer,
    QualificationListSerializer,
    QualificationSerializer,
)


class QualificationSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inst = Institution.objects.create(
            name='University of Johannesburg', abbreviation='UJ',
        )
        cls.qual = Qualification.objects.create(
            institution=cls.inst,
            slug='uj-ba-interior-design',
            name='BA Interior Design',
            qualification_code='B8BA6Q',
            faculty='Art, Design and Architecture',
            description='Interior design qualification.',
            minimum_aps=25,
        )
        rule = APSRule.objects.create(
            qualification=cls.qual,
            rule_type='subject_dependent_minimum_aps',
        )
        APSRuleCondition.objects.create(
            rule=rule, subject='Mathematics', minimum_level=4, min_aps=25,
        )
        APSRuleCondition.objects.create(
            rule=rule, subject='Mathematical Literacy', minimum_level=5, min_aps=26,
        )
        SubjectRequirement.objects.create(
            qualification=cls.qual, requirement_type='mandatory',
            subject='English', minimum_level=5,
        )
        SubjectRequirement.objects.create(
            qualification=cls.qual, requirement_type='one_of',
            subject='Mathematics', minimum_level=4,
        )
        SubjectRequirement.objects.create(
            qualification=cls.qual, requirement_type='disallowed',
            subject='Technical Mathematics', minimum_level=0,
        )
        SelectionRequirement.objects.create(
            qualification=cls.qual, selection_type='possible_portfolio',
            required=False, notes=None,
        )

    def test_detail_fields(self):
        data = QualificationSerializer(self.qual).data
        expected_keys = {
            'id', 'slug', 'name', 'qualification_code', 'faculty',
            'description', 'minimum_aps', 'aps_rules',
            'subject_requirements', 'selection_requirements',
        }
        self.assertEqual(set(data.keys()), expected_keys)

    def test_aps_rules_nested(self):
        data = QualificationSerializer(self.qual).data
        self.assertEqual(len(data['aps_rules']), 1)
        rule = data['aps_rules'][0]
        self.assertEqual(rule['rule_type'], 'subject_dependent_minimum_aps')
        self.assertEqual(len(rule['conditions']), 2)
        self.assertEqual(rule['conditions'][0]['subject'], 'Mathematics')

    def test_subject_requirements_grouped(self):
        data = QualificationSerializer(self.qual).data
        sr = data['subject_requirements']
        self.assertEqual(len(sr['mandatory']), 1)
        self.assertEqual(sr['mandatory'][0]['subject'], 'English')
        self.assertEqual(len(sr['one_of']), 1)
        self.assertEqual(len(sr['disallowed']), 1)
        self.assertEqual(sr['disallowed'][0]['subject'], 'Technical Mathematics')

    def test_selection_requirements(self):
        data = QualificationSerializer(self.qual).data
        self.assertEqual(len(data['selection_requirements']), 1)
        self.assertEqual(data['selection_requirements'][0]['type'], 'possible_portfolio')
        self.assertFalse(data['selection_requirements'][0]['required'])

    def test_list_serializer_fields(self):
        data = QualificationListSerializer(self.qual).data
        self.assertIn('institution_name', data)
        self.assertIn('institution_abbr', data)
        self.assertEqual(data['institution_abbr'], 'UJ')
        self.assertNotIn('aps_rules', data)
        self.assertNotIn('subject_requirements', data)

    def test_institution_detail_serializer(self):
        data = InstitutionDetailSerializer(self.inst).data
        self.assertEqual(data['name'], 'University of Johannesburg')
        self.assertEqual(len(data['qualifications']), 1)
