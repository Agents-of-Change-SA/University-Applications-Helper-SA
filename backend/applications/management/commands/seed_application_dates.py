from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from applications.models import ApplicationEntry

SEED_DATA = [
    {
        'institution_name': 'University of Cape Town',
        'open_date': date(2026, 3, 1),
        'close_date': date(2026, 6, 30),
        'application_fee': Decimal('100.00'),
        'portal_url': 'https://applyonline.uct.ac.za',
    },
    {
        'institution_name': 'University of the Witwatersrand',
        'open_date': date(2026, 4, 1),
        'close_date': date(2026, 9, 30),
        'application_fee': Decimal('200.00'),
        'portal_url': 'https://self-service.wits.ac.za',
    },
    {
        'institution_name': 'Stellenbosch University',
        'open_date': date(2026, 5, 1),
        'close_date': date(2026, 8, 31),
        'application_fee': Decimal('100.00'),
        'portal_url': 'https://apps.sun.ac.za',
    },
    {
        'institution_name': 'University of Pretoria',
        'open_date': date(2026, 1, 15),
        'close_date': date(2026, 7, 31),
        'application_fee': Decimal('300.00'),
        'portal_url': 'https://www.up.ac.za/apply',
    },
    {
        'institution_name': 'University of KwaZulu-Natal',
        'open_date': date(2026, 6, 1),
        'close_date': date(2026, 10, 31),
        'application_fee': Decimal('250.00'),
        'portal_url': 'https://applications.ukzn.ac.za',
    },
    {
        'institution_name': 'Durban University of Technology',
        'open_date': date(2025, 9, 1),
        'close_date': date(2025, 11, 30),
        'application_fee': Decimal('0.00'),
        'portal_url': 'https://www.dut.ac.za/apply',
    },
    {
        'institution_name': 'University of Johannesburg',
        'open_date': date(2026, 2, 1),
        'close_date': date(2026, 10, 31),
        'application_fee': Decimal('0.00'),
        'portal_url': 'https://www.uj.ac.za/apply',
    },
]


class Command(BaseCommand):
    help = 'Seed the database with initial application date entries for 7 SA institutions.'

    def handle(self, *args, **options):
        for entry_data in SEED_DATA:
            obj, created = ApplicationEntry.objects.update_or_create(
                institution_name=entry_data['institution_name'],
                defaults=entry_data,
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action}: {obj.institution_name}'))
