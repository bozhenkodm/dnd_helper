from django.contrib import admin

from base.admin.admin_classes import (
    ArmorAdmin,
    ArmorTypeAdmin,
    ArmsItemSlotAdmin,
    ClassAdmin,
    EncounterAdmin,
    FunctionalTemplateAdmin,
    MagicArmItemTypeAdmin,
    MagicArmorTypeAdmin,
    MagicItemAdmin,
    MagicItemTypeAdmin,
    MagicWeaponTypeAdmin,
    NPCAdmin,
    ParagonPathAdmin,
    PlayerCharactersAdmin,
    PowerAdmin,
    RaceAdmin,
    WeaponAdmin,
    WeaponTypeAdmin,
)
from base.models.bonuses import Bonus
from base.models.encounters import Encounter, PlayerCharacters
from base.models.magic_items import (
    ArmsSlotItem,
    MagicArmItemType,
    MagicArmorType,
    MagicItemType,
    MagicWeaponType,
    SimpleMagicItem,
)
from base.models.models import (
    NPC,
    Armor,
    ArmorType,
    Class,
    FunctionalTemplate,
    ParagonPath,
    Race,
    Weapon,
    WeaponType,
)
from base.models.powers import Power

admin.site.register(Race, RaceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(NPC, NPCAdmin)
admin.site.register(ParagonPath, ParagonPathAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(ArmorType, ArmorTypeAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(WeaponType, WeaponTypeAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Power, PowerAdmin)
admin.site.register(FunctionalTemplate, FunctionalTemplateAdmin)
admin.site.register(PlayerCharacters, PlayerCharactersAdmin)
admin.site.register(MagicItemType, MagicItemTypeAdmin)
admin.site.register(MagicArmorType, MagicArmorTypeAdmin)
admin.site.register(MagicWeaponType, MagicWeaponTypeAdmin)
admin.site.register(MagicArmItemType, MagicArmItemTypeAdmin)
admin.site.register(SimpleMagicItem, MagicItemAdmin)
admin.site.register(ArmsSlotItem, ArmsItemSlotAdmin)
admin.site.register(Bonus)
