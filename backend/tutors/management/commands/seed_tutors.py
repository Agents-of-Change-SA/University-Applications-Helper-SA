from django.core.management.base import BaseCommand

from tutors.models import Tutor

SEED_DATA = [
    {'name': 'Thabo Mokoena', 'subject': 'Mathematics', 'contact': '+27 XX XXX XXXX'},
    {'name': 'Naledi Dlamini', 'subject': 'Physical Sciences', 'contact': '+27 XX XXX XXXX'},
    {'name': 'Sipho Nkosi', 'subject': 'Accounting', 'contact': '+27 XX XXX XXXX'},
    {'name': 'Lerato Molefe', 'subject': 'English', 'contact': '+27 XX XXX XXXX'},
    {'name': 'Ayanda Zulu', 'subject': 'Life Sciences', 'contact': '+27 XX XXX XXXX'},
    {'name': 'Kagiso Patel', 'subject': 'Information Technology', 'contact': '+27 XX XXX XXXX'},
]


class Command(BaseCommand):
    help = 'Seed the database with initial tutor data.'

    def handle(self, *args, **options):
        for data in SEED_DATA:
            obj, created = Tutor.objects.update_or_create(
                name=data['name'],
                defaults=data,
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action}: {obj.name}'))
