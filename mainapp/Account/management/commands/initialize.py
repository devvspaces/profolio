from django.core.management.base import BaseCommand, CommandError

# Python script to setup projects
import os
from secrets import choice
from django.conf import settings


def create_logs():
    """Create logs directory"""
    path = settings.BASE_DIR / "logs"
    if not os.path.exists(path):
        os.makedirs(path)


def create_strong_secret_key():
    """Create a strong secret key"""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(choice(chars) for _ in range(50))


def create_env():
    """Create .env file"""
    path = settings.BASE_DIR / ".env"
    with open(path, "w") as env_file:
        secret_key = create_strong_secret_key()
        text = f"SECRET_KEY={secret_key}"
        env_file.write(text)



class Command(BaseCommand):
    help = 'Command to initialize project'

    def _write_success(self, message: str):
        self.stdout.write(
            self.style.SUCCESS(message))

    def handle(self, *args, **options):
        try:
            # 1. Create logs directory
            create_logs()

            # 2. Create .env file
            create_env()

            self._write_success("Project initialized successfully")

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise CommandError(e)
