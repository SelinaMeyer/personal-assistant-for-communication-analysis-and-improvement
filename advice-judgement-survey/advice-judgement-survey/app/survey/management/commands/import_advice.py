from django.core.management.base import BaseCommand
import csv
from survey.models import Advice, Chat

class Command(BaseCommand):
    help = 'Imports advice data from a CSV file into the database.'

    def add_arguments(self, parser):
        # Optional: add arguments here, if you need to specify a file path or other options
        parser.add_argument('csv_file_path', type=str, help='Path to the CSV file containing advice data.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']  # Use this if you've added an argument for file path
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                chat, _ = Chat.objects.get_or_create(
                    chat_id=row['Chat_id'],
                    defaults={'chat_text': 'Default chat text here'}  # Adjust as needed
                )
                Advice.objects.get_or_create(
                    advice_id=row['Advise_id'],
                    chat=chat,
                    defaults={
                        'advice_text': row['Advice'],
                        'context': row['Advice Type'],
                        'model': row["Model"]
                        # add other fields as necessary
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported advice data from CSV.'))