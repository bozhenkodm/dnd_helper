from django.contrib import admin

from base.admin.admin_classes import (
    ArmorAdmin,
    BonusAdmin,
    BookAdmin,
    BookSourceAdmin,
    ClassAdmin,
    ConstraintAdmin,
    EncounterAdmin,
    FeatAdmin,
    FunctionalTemplateAdmin,
    NPCAdmin,
    ParagonPathAdmin,
    PlayerCharactersAdmin,
    PowerAdmin,
    RaceAdmin,
    SubclassAdmin,
    WeaponAdmin,
    WeaponStateAdmin,
    WeaponTypeAdmin,
)
from base.models.bonuses import Bonus
from base.models.books import Book, BookSource
from base.models.condition import Constraint
from base.models.encounters import Encounter, Party, PlayerCharacter
from base.models.feats import Feat, WeaponState
from base.models.klass import Class, Subclass
from base.models.models import (
    NPC,
    Armor,
    FunctionalTemplate,
    ParagonPath,
    Race,
    Weapon,
    WeaponType,
)
from base.models.powers import Power

admin.site.register(Race, RaceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subclass, SubclassAdmin)
admin.site.register(NPC, NPCAdmin)
admin.site.register(ParagonPath, ParagonPathAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Party)
admin.site.register(FunctionalTemplate, FunctionalTemplateAdmin)
admin.site.register(PlayerCharacter, PlayerCharactersAdmin)


# for autocomplete fields
admin.site.register(WeaponType, WeaponTypeAdmin)
admin.site.register(Power, PowerAdmin)
admin.site.register(Feat, FeatAdmin)


# hidden from sidebar
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(WeaponState, WeaponStateAdmin)
admin.site.register(Constraint, ConstraintAdmin)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookSource, BookSourceAdmin)
