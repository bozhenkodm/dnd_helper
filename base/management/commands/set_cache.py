from django.core.management import BaseCommand

from base.models.models import NPC


class Command(BaseCommand):
    help = 'Set bonuses cache'

    def handle(self, *args, **options):
        for npc in NPC.objects.all():
            npc.cache_bonuses()
            self.stdout.write(self.style.SUCCESS(f'{npc.name} bonuses has been cached'))
            npc.cache_powers()
            self.stdout.write(self.style.SUCCESS(f'{npc.name} powers has been cached'))
