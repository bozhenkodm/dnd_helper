from random import choice

from django.core.management import BaseCommand

from base.models import Class, Race


class Command(BaseCommand):
    help = 'Gets random npc'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        race = choice(Race.objects.all())
        klass = choice(Class.objects.all())
        self.stdout.write(
            self.style.SUCCESS(
                '%s; %s' % (race.get_name_display(), klass.get_name_display())
            )
        )
