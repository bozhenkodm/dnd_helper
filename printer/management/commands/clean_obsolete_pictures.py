import os.path

from django.conf import settings
from django.core.management import BaseCommand

from printer.models import Avatar, GridMap, Zone


class Command(BaseCommand):
    help = 'Generate random abilities'

    def handle(self, *args, **options):
        models = (
            (Avatar, 'base_image'),
            (Zone, 'image'),
            (GridMap, 'base_image'),
        )

        for model, image_field in models:
            folder = os.path.join(
                settings.MEDIA_ROOT,
                model._meta.get_field(image_field).upload_to,
            )
            obsolete_pictures = []
            for image in os.listdir(folder):
                if not model.objects.filter(
                    **{f'{image_field}__endswith': image}
                ).exists():
                    obsolete_pictures.append(image)
            self.stdout.write(self.style.SUCCESS(f'{folder}:'))
            for obsolete_picture in obsolete_pictures:
                full_path = os.path.join(folder, obsolete_picture)
                os.remove(full_path)
                self.stdout.write(
                    self.style.SUCCESS(f'{obsolete_picture} has been removed')
                )
