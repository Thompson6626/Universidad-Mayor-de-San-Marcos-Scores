from django.core.management.base import BaseCommand
from typing import Any
from django.conf import settings

import asyncio
import os
from helpers import fetch


CSV_SCORES_PATH = getattr(settings, 'CSV_SCORES_PATH')

UNMSM_URL_RESULTS = {
    "2023-II": "https://admision.unmsm.edu.pe/WebsiteExa_20232/",
    "2024-I": "https://admision.unmsm.edu.pe/Website20241/",
    "2024-II": "https://admision.unmsm.edu.pe/Website20242/index.html",
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Delete and re-fetch score data if file already exists'
        )

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Fetching scores...")
        # Deleting if it exists
        if os.path.exists(CSV_SCORES_PATH):
             if options["replace"]:
                self.stdout.write(self.style.WARNING('File found, replacing...'))
                os.remove(CSV_SCORES_PATH)
             else:
                self.stdout.write(self.style.WARNING('File found, skipping...'))
                return

        try:
            fetch(UNMSM_URL_RESULTS, CSV_SCORES_PATH)
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to fetch scores'))
        else:
            self.stdout.write(self.style.SUCCESS('Scores successfully fetched'))

