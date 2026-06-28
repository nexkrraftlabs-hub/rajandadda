import os
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from home.models import Fleet, Destination, AdminProfile


class Command(BaseCommand):
    help = "Upload existing local media to Cloudinary"

    def upload_field(self, obj, field_name, label):
        field = getattr(obj, field_name)

        if not field:
            return

        # Local file path
        local_path = os.path.join(settings.MEDIA_ROOT, field.name)

        if not os.path.exists(local_path):
            self.stdout.write(
                self.style.WARNING(f"❌ File not found: {local_path}")
            )
            return

        with open(local_path, "rb") as f:
            field.save(
                os.path.basename(local_path),
                File(f),
                save=True,
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Uploaded {label}"))

    def handle(self, *args, **kwargs):

        self.stdout.write("\nUploading Fleet Images...\n")

        for fleet in Fleet.objects.all():
            self.upload_field(fleet, "image", fleet.name)

        self.stdout.write("\nUploading Destination Images...\n")

        for d in Destination.objects.all():
            self.upload_field(d, "image", d.name)

        self.stdout.write("\nUploading Profile Images...\n")

        for p in AdminProfile.objects.all():
            self.upload_field(p, "profile_image", p.user.username)

        self.stdout.write(
            self.style.SUCCESS("\n🎉 All media uploaded successfully.")
        )