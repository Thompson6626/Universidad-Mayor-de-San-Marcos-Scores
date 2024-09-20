from django.core.management.base import BaseCommand
from typing import Any
from django.conf import settings
import os
from helpers import populate_database

CSV_SCORES_PATH = getattr(settings, 'CSV_SCORES_PATH')
BATCH_SIZE = 1000

class Command(BaseCommand):
    help = 'Populates database with data from the CSV file created by the fetch_scores command'

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Populating database...")
        if os.path.exists(CSV_SCORES_PATH):
            self.stdout.write(self.style.SUCCESS('File found, populating database...'))
        else:
            self.stdout.write(self.style.WARNING('CSV file not found, skipping...'))
            return

        success = populate_database(CSV_SCORES_PATH, BATCH_SIZE)

        if success:
            self.stdout.write(self.style.SUCCESS('Database successfully populated'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to populate database: {e}'))

