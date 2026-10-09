import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ["DEPLOY_ADMIN_USERNAME"]
        password = os.environ["DEPLOY_ADMIN_PASSWORD"]

        if User.objects.filter(username=username).exists():
            self.stdout.write("Username already exists.")
            return

        User.objects.create_superuser(
            username=username,
            email="",
            password=password,
        )
        self.stdout.write("Admin created successfully.")