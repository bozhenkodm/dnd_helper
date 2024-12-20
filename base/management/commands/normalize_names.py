from django.core.management import BaseCommand

from base.models.feats import Feat


class Command(BaseCommand):
    help = 'Generate random abilities'

    def handle(self, *args, **options):
        for feat in Feat.objects.all():
            feat.name = feat.name.lower().capitalize().strip()
            feat.text = ' '.join(feat.text.split()).strip()
            feat.save()
            self.stdout.write(self.style.SUCCESS(f'{feat.name} normalized'))
