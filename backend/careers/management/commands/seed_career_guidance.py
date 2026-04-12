from django.core.management.base import BaseCommand

from careers.models import CareerGuidanceEntry

SEED_DATA = [
    ('Software Engineer', 'Mathematics', 'Core requirement for CS degrees and logical thinking'),
    ('Software Engineer', 'Information Technology', 'Direct exposure to programming concepts'),
    ('Software Engineer', 'Physical Sciences', 'Develops analytical and problem-solving skills'),
    ('Doctor', 'Life Sciences', 'Essential foundation for medical studies'),
    ('Doctor', 'Physical Sciences', 'Required for MBChB admission at most universities'),
    ('Doctor', 'Mathematics', 'Needed for medical degree entry requirements'),
    ('Lawyer', 'English', 'Critical for legal writing, argumentation, and comprehension'),
    ('Lawyer', 'History', 'Builds understanding of legal systems and precedent'),
    ('Lawyer', 'Mathematics', 'Supports logical reasoning and analytical thinking'),
    ('Accountant', 'Accounting', 'Direct prerequisite for BCom Accounting degrees'),
    ('Accountant', 'Mathematics', 'Essential for financial calculations and analysis'),
    ('Accountant', 'English', 'Important for business communication and reporting'),
    ('Teacher', 'English', 'Foundation for communication and instruction'),
    ('Teacher', 'Mathematics', 'Widely needed subject for education degrees'),
    ('Teacher', 'Life Orientation', 'Supports understanding of learner development'),
]


class Command(BaseCommand):
    help = 'Seed the database with career guidance entries.'

    def handle(self, *args, **options):
        for aspiration, subject, explanation in SEED_DATA:
            obj, created = CareerGuidanceEntry.objects.update_or_create(
                aspiration=aspiration,
                subject=subject,
                defaults={'explanation': explanation},
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(
                f'{action}: {obj.aspiration} -> {obj.subject}'
            ))
