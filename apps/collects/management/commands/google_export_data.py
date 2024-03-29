from django.core.management.base import BaseCommand

from utils.export_database import export_to_google_sheets


class Command(BaseCommand):
    help = 'Export data from database to Google Sheets'

    def handle(self, *args, **kwargs):
        export_to_google_sheets()
        self.stdout.write(
            self.style.SUCCESS('Data exported to Google Sheets successfully.'))
