from django.core.management.base import BaseCommand
from typing import Any
from django.conf import settings

import asyncio

from helpers import fetch


CSV_SCORES_PATH = getattr(settings, 'CSV_SCORES_PATH')

UNMSM_URL_RESULTS = {
    "2024-I": "https://admision.unmsm.edu.pe/Website20241/",
    "2024-II": "https://admision.unmsm.edu.pe/Website20242/index.html",
}


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Fetching score data...")
        try:
            fetch(UNMSM_URL_RESULTS, CSV_SCORES_PATH)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR('Failed to fetch scores')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('Scores successfully fetched')
        )

