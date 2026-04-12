from django.core.management.base import BaseCommand

from qualifications.models import (
    APSRule,
    APSRuleCondition,
    Institution,
    Qualification,
    SelectionRequirement,
    SubjectRequirement,
)

SEED_DATA = [
    {
        'name': 'University of Johannesburg',
        'abbreviation': 'UJ',
        'qualifications': [
            {
                'slug': 'uj-ba-interior-design',
                'name': 'BA Interior Design',
                'qualification_code': 'B8BA6Q',
                'faculty': 'Art, Design and Architecture',
                'description': (
                    'Interior Designers engage with a range of interior spaces '
                    'to create innovative spatial solutions with a thorough '
                    'knowledge of building technology, materials and human '
                    'environment needs.'
                ),
                'minimum_aps': 25,
                'aps_rules': [
                    {
                        'type': 'subject_dependent_minimum_aps',
                        'conditions': [
                            {'subject': 'Mathematics', 'minimum_level': 4, 'min_aps': 25},
                            {'subject': 'Mathematical Literacy', 'minimum_level': 5, 'min_aps': 26},
                        ],
                    },
                ],
                'subject_requirements': {
                    'mandatory': [
                        {'subject': 'English', 'minimum_level': 5},
                    ],
                    'one_of': [
                        {'subject': 'Mathematics', 'minimum_level': 4},
                        {'subject': 'Mathematical Literacy', 'minimum_level': 5},
                    ],
                    'disallowed': [
                        {'subject': 'Technical Mathematics', 'minimum_level': 0},
                    ],
                },
                'selection_requirements': [
                    {'type': 'possible_portfolio', 'required': False, 'notes': None},
                ],
            },
        ],
    },
    {
        'name': 'University of Cape Town',
        'abbreviation': 'UCT',
        'qualifications': [
            {
                'slug': 'uct-bsc-computer-science',
                'name': 'BSc Computer Science',
                'qualification_code': 'SC016',
                'faculty': 'Science',
                'description': 'Study of computation, algorithms, and information systems.',
                'minimum_aps': 34,
                'aps_rules': [],
                'subject_requirements': {
                    'mandatory': [
                        {'subject': 'Mathematics', 'minimum_level': 5},
                        {'subject': 'English', 'minimum_level': 4},
                    ],
                    'one_of': [],
                    'disallowed': [],
                },
                'selection_requirements': [],
            },
        ],
    },
    {
        'name': 'Stellenbosch University',
        'abbreviation': 'SU',
        'qualifications': [
            {
                'slug': 'su-beng-electrical',
                'name': 'BEng Electrical and Electronic Engineering',
                'qualification_code': 'EE001',
                'faculty': 'Engineering',
                'description': 'Electrical and electronic engineering fundamentals.',
                'minimum_aps': 36,
                'aps_rules': [],
                'subject_requirements': {
                    'mandatory': [
                        {'subject': 'Mathematics', 'minimum_level': 6},
                        {'subject': 'Physical Sciences', 'minimum_level': 5},
                        {'subject': 'English', 'minimum_level': 4},
                    ],
                    'one_of': [],
                    'disallowed': [],
                },
                'selection_requirements': [
                    {'type': 'nbt', 'required': True, 'notes': 'NBT Mathematics and Academic Literacy required'},
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with qualification data.'

    def handle(self, *args, **options):
        for inst_data in SEED_DATA:
            institution, created = Institution.objects.update_or_create(
                name=inst_data['name'],
                defaults={'abbreviation': inst_data['abbreviation']},
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action} institution: {institution.name}'))

            for qual_data in inst_data['qualifications']:
                qual, created = Qualification.objects.update_or_create(
                    slug=qual_data['slug'],
                    defaults={
                        'institution': institution,
                        'name': qual_data['name'],
                        'qualification_code': qual_data['qualification_code'],
                        'faculty': qual_data['faculty'],
                        'description': qual_data['description'],
                        'minimum_aps': qual_data['minimum_aps'],
                    },
                )
                action = 'Created' if created else 'Updated'
                self.stdout.write(f'  {action} qualification: {qual.name}')

                # Clear and re-create related objects
                qual.aps_rules.all().delete()
                qual.subject_requirements.all().delete()
                qual.selection_requirements.all().delete()

                for rule_data in qual_data.get('aps_rules', []):
                    rule = APSRule.objects.create(
                        qualification=qual,
                        rule_type=rule_data['type'],
                    )
                    for cond in rule_data['conditions']:
                        APSRuleCondition.objects.create(rule=rule, **cond)

                for req_type in ('mandatory', 'one_of', 'disallowed'):
                    for req in qual_data.get('subject_requirements', {}).get(req_type, []):
                        SubjectRequirement.objects.create(
                            qualification=qual,
                            requirement_type=req_type,
                            **req,
                        )

                for sel in qual_data.get('selection_requirements', []):
                    SelectionRequirement.objects.create(
                        qualification=qual,
                        selection_type=sel['type'],
                        required=sel['required'],
                        notes=sel.get('notes'),
                    )
