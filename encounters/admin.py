from django.contrib import admin

from base.admin.admin_classes import EncounterAdmin, PlayerCharactersAdmin
from encounters.models import Avatar, Encounter, GridMap, Party, PlayerCharacter
from printer.admin import AvatarAdmin, GridMapAdmin

admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Party)
admin.site.register(PlayerCharacter, PlayerCharactersAdmin)

admin.site.register(GridMap, GridMapAdmin)
admin.site.register(Avatar, AvatarAdmin)
