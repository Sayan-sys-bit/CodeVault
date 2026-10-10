
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from blog.models import Post


class Command(BaseCommand):
    help = "Import blog posts from posts.json without duplicating existing posts."

    def handle(self, *args, **options):
        file_path = Path("posts.json")

        if not file_path.exists():
            raise CommandError("posts.json was not found in the project root.")

        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as exc:
            raise CommandError(f"Could not read posts.json: {exc}")

        records = [
            item for item in data
            if item.get("model", "").lower() == "blog.post"
        ]

        if not records:
            raise CommandError("No blog.post records found in posts.json.")

        created = 0
        skipped = 0

        with transaction.atomic():
            for record in records:
                fields = record.get("fields", {})
                post_id = record.get("pk") or fields.get("sno")

                if not post_id:
                    skipped += 1
                    continue

                if Post.objects.filter(pk=post_id).exists():
                    skipped += 1
                    continue

                post = Post(
                    sno=post_id,
                    title=fields["title"],
                    slug=fields["slug"],
                    author=fields["author"],
                    content=fields["content"],
                )

                # Preserve the original timestamp from the export.
                timestamp = fields.get("timeStamp")
                if timestamp:
                    from django.utils.dateparse import parse_datetime
                    parsed_timestamp = parse_datetime(timestamp)
                    if parsed_timestamp:
                        post.timeStamp = parsed_timestamp

                post.save(force_insert=True)
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete. Created: {created}; skipped: {skipped}."
            )
        )
