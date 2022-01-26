from django.contrib import admin
from django.contrib.auth.models import Group, User

from base.admin.admin_class import (
    ArmorAdmin,
    ClassAdmin,
    EncounterAdmin,
    FunctionalTemplateAdmin,
    MagicItemAdmin,
    NPCAdmin,
    PlayerCharactersAdmin,
    PowerAdmin,
    RaceAdmin,
    WeaponAdmin,
    WeaponTypeAdmin,
)
from base.models import Encounter
from base.models.encounters import PlayerCharacters
from base.models.magic_items import MagicItem
from base.models.models import (
    NPC,
    Armor,
    Class,
    FunctionalTemplate,
    Race,
    Weapon,
    WeaponType,
)
from base.models.powers import Power

admin.site.register(Race, RaceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(NPC, NPCAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(WeaponType, WeaponTypeAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Power, PowerAdmin)
admin.site.register(FunctionalTemplate, FunctionalTemplateAdmin)
admin.site.register(PlayerCharacters, PlayerCharactersAdmin)
admin.site.register(MagicItem, MagicItemAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
