from random import choice

from django.core.management import BaseCommand

from base.models import Class, Race


class Command(BaseCommand):
    help = 'Parse powers from rules pdf into csv file'

    def add_arguments(self, parser):
        parser.add_argument('class', type=str)
        parser.add_argument('start_word', type=str)
        parser.add_argument('--start', type=int)
        parser.add_argument('--end', type=int)
        parser.add_argument('--output', type=str)

    def handle(self, *args, **options):
        if options.get('all'):
            race = choice(Race.objects.all())
        else:
            race = choice(Race.objects.filter(is_sociable=True))
        klass = choice(Class.objects.all())
        self.stdout.write(
            self.style.SUCCESS(
                '%s; %s' % (race.get_name_display(), klass.get_name_display())
            )
        )
