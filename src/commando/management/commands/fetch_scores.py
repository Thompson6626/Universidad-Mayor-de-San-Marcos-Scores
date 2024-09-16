from django.core.management.base import BaseCommand
from typing import Any
from django.conf import settings

import asyncio

from helpers import fetch_scores


CSV_SCORES_PATH = getattr(settings, 'CSV_SCORES_PATH')

UNMSM_URL_RESULTS = {
    "2024-I": "https://admision.unmsm.edu.pe/Website20241/",
    "2024-II": "https://admision.unmsm.edu.pe/Website20242/index.html",
}


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        asyncio.run(self.async_handle(*args, **options))

    async def async_handle(self, *args: Any, **options: Any):
        self.stdout.write("Fetching score data")
        
        # Await the async function to fetch and populate data
        await fetch_scores(UNMSM_URL_RESULTS, CSV_SCORES_PATH)

        self.stdout.write(
                self.style.SUCCESS('Successfully fetched scores')
            )
        
