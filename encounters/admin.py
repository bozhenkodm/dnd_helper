from django.contrib import admin

from base.admin.admin_classes import EncounterAdmin, MonsterAdmin, PlayerCharactersAdmin
from encounters.models import (
    Avatar,
    Encounter,
    GridMap,
    Monster,
    Party,
    PlayerCharacter,
)
from printer.admin import AvatarAdmin, GridMapAdmin

admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Party)
admin.site.register(PlayerCharacter, PlayerCharactersAdmin)
admin.site.register(Monster, MonsterAdmin)

admin.site.register(GridMap, GridMapAdmin)
admin.site.register(Avatar, AvatarAdmin)
