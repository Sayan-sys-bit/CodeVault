import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Temporarily recover a Django production admin account"

    def handle(self, *args, **options):
        username = os.environ.get("RECOVERY_USERNAME")
        password = os.environ.get("RECOVERY_PASSWORD")

        if not username or not password:
            raise CommandError("Recovery environment variables are required.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"is_staff": True, "is_superuser": True},
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS("Admin recovery completed.")
        )