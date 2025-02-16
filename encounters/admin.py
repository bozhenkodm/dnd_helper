from django.contrib import admin

from base.admin.admin_classes import EncounterAdmin, PlayerCharactersAdmin
from encounters.models import Encounter, Party, PlayerCharacter

admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Party)
admin.site.register(PlayerCharacter, PlayerCharactersAdmin)
