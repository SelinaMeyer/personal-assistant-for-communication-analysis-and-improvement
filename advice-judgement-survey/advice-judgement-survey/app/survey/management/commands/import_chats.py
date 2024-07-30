"""
Django Command to import the pre-generated Chats from a CSV file
"""

from django.core.management.base import BaseCommand
import csv
from survey.models import Chat

class Command(BaseCommand):
    help = 'Imports chats from a CSV file, updating existing records as necessary.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="The path to the CSV file to import.")

    def handle(self, *args, **options):
        file_path = options['csv_file']
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                chat_id = row['Chat_id']
                chat_text = row['chat_text']
                victim = row['Victim']
                culprit = row["culprit"]
                interaction_context = row["context"]
                manipulation_strategy = row["manipulation_strategy"]
                # Attempt to get the chat by ID
                chat, created = Chat.objects.get_or_create(
                    chat_id=chat_id,
                    defaults={'chat_text': chat_text}
                )
                # If the chat was not created, it already existed, and we may need to update it
                if not created:
                    chat.chat_text = chat_text
                    chat.victim = victim
                    chat.culprit = culprit
                    chat.manipulation_strategy = manipulation_strategy
                    chat.interaction_context = interaction_context
                    chat.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated existing chat: {chat_id}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Added new chat: {chat_id}'))