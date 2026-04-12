"""
Management command to load qualifications from a JSON file into the database.

Usage:
    python manage.py load_qualifications path/to/uj_all_pages.json
    python manage.py load_qualifications path/to/file.json --dry-run
"""
from django.core.management.base import BaseCommand, CommandError

from qualifications.readers.json_loader import load_from_json


class Command(BaseCommand):
    help = 'Load qualifications from a Univice-format JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to the JSON file to load',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            help='Validate without writing to the database',
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        dry_run = options['dry_run']

        try:
            stats = load_from_json(
                source=json_file,
                dry_run=dry_run,
                log_fn=lambda msg: self.stdout.write(msg),
            )
        except FileNotFoundError as e:
            raise CommandError(str(e))
        except ValueError as e:
            raise CommandError(str(e))

        if stats['errors']:
            self.stderr.write(
                self.style.WARNING(f"{len(stats['errors'])} errors occurred")
            )

        self.stdout.write(self.style.SUCCESS(
            f"Qualifications: {stats['qualifications_created']} created, "
            f"{stats['qualifications_updated']} updated, "
            f"{stats['qualifications_skipped']} skipped"
        ))
