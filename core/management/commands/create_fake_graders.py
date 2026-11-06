import json
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create grader accounts from the GRADER_ACCOUNTS_JSON environment variable."

    def handle(self, *args, **options):
        raw_accounts = os.getenv("GRADER_ACCOUNTS_JSON")
        if not raw_accounts:
            raise CommandError("Set GRADER_ACCOUNTS_JSON to a JSON list of username/password objects.")

        try:
            accounts = json.loads(raw_accounts)
        except json.JSONDecodeError as error:
            raise CommandError("GRADER_ACCOUNTS_JSON must contain valid JSON.") from error

        if not isinstance(accounts, list):
            raise CommandError("GRADER_ACCOUNTS_JSON must be a JSON list.")

        user_model = get_user_model()
        created_count = 0
        for account in accounts:
            if not isinstance(account, dict):
                raise CommandError("Each grader account must be an object.")
            username = account.get("username")
            password = account.get("password")
            if not isinstance(username, str) or not username.strip():
                raise CommandError("Each grader account must have a non-empty username.")
            if not isinstance(password, str) or not password:
                raise CommandError("Each grader account must have a non-empty password.")

            if not user_model.objects.filter(username=username).exists():
                user_model.objects.create_user(username=username, password=password)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} grader account(s)."))
