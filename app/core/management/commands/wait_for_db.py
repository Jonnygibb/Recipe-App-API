"""
Django command to wait for database to be available.
"""

import time

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        # Log message to screen.
        self.stdout.write('Waiting for Database...')
        db_up = False
        while db_up is False:
            try:
                # If database is not ready, error will be thrown.
                self.check(databases=['default'])
                # Mark db as ready and exit loop.
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                # Wait 1 second before attempting to check database status.
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
