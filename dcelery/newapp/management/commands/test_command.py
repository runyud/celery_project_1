from typing import Any
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Description of the command"

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("This is my simple task")
