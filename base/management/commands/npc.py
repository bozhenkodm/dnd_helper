from random import choice

from django.core.management import BaseCommand

from base.models import Race
from base.models.klass import Class


class Command(BaseCommand):
    help = 'Gets random npc'

    def add_arguments(self, parser):
        parser.add_argument('--all', type=bool)

    def handle(self, *args, **options):
        if options.get('all'):
            race = choice(Race.objects.all())
        else:
            race = choice(Race.objects.filter(is_social=True))
        klass = choice(Class.objects.all())
        self.stdout.write(
            self.style.SUCCESS(
                '%s; %s' % (race.get_name_display(), klass.get_name_display())
            )
        )
