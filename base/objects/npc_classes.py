from typing import ClassVar, Sequence

from base.constants.constants import (
    ArmorTypeIntEnum,
    NPCClassIntEnum,
    PowerSourceEnum,
    ShieldTypeEnum,
    SkillsEnum,
    WeaponCategoryIntEnum,
)
from base.objects.skills import Skills
from base.objects.weapon_types import WeaponType


class NPCClass:
    slug: ClassVar[NPCClassIntEnum] = None
    power_source: ClassVar[PowerSourceEnum]
    fortitude: ClassVar[int] = 0
    reflex: ClassVar[int] = 0
    will: ClassVar[int] = 0
    mandatory_skills: ClassVar[Skills] = Skills()
    trainable_skills: ClassVar[Skills] = Skills()
    skill_bonuses: ClassVar[Skills] = Skills()
    available_armor_types: ClassVar[Sequence[ArmorTypeIntEnum]] = ()
    available_shield_types: ClassVar[Sequence[ShieldTypeEnum]] = ()
    available_weapon_categories: ClassVar[Sequence[WeaponCategoryIntEnum]] = ()
    available_weapon_types: ClassVar[Sequence[WeaponType]]
    # available_implement_types
    hit_points_per_level: ClassVar[int] = 8

    def hit_points_bonus(self, **kwargs):
        return 0

    def attack_bonus(self, **kwargs):
        return 0

    def armor_class_bonus(self, **kwargs):
        return 0


class InvokerClass(NPCClass):
    slug = NPCClassIntEnum.INVOKER
    power_source = PowerSourceEnum.DIVINE
    hit_points_per_level = 6


class ArtificerClass(NPCClass):
    slug = NPCClassIntEnum.ARTIFICER
    power_source = PowerSourceEnum.ARCANE
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        perception=5, thievery=5, history=5, diplomacy=5, dungeoneering=5, heal=5
    )
    fortitude = 1
    will = 1


class BardClass(NPCClass):
    slug = NPCClassIntEnum.BARD
    power_source = PowerSourceEnum.ARCANE
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        acrobatics=5,
        athletics=5,
        perception=5,
        intimidate=5,
        streetwise=5,
        history=5,
        bluff=5,
        diplomacy=5,
        nature=5,
        dungeoneering=5,
        insight=5,
        religion=5,
        heal=5,
    )
    skill_bonuses = Skills.init_with_const(SkillsEnum, 1)
    reflex = 1
    will = 1


class VampireClass(NPCClass):
    slug = NPCClassIntEnum.VAMPIRE
    power_source = PowerSourceEnum.SHADOW


class BarbarianClass(NPCClass):
    slug = NPCClassIntEnum.BARBARIAN
    power_source = PowerSourceEnum.PRIMAL
    trainable_skills = Skills(
        acrobatics=5,
        athletics=5,
        endurance=5,
        perception=5,
        intimidate=5,
        nature=5,
        heal=5,
    )
    fortitude = 2


class WarlordClass(NPCClass):
    slug = NPCClassIntEnum.WARLORD
    power_source = PowerSourceEnum.MARTIAL
    fortitude = 1
    will = 1
    trainable_skills = Skills(athletics=5, endurance=5, intimidate=5, history=5, diplomacy=5, heal=5)


class FighterClass(NPCClass):
    slug = NPCClassIntEnum.FIGHTER
    power_source = PowerSourceEnum.MARTIAL
    fortitude = 2
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, streetwise=5, heal=5
    )


class WizardClass(NPCClass):
    slug = NPCClassIntEnum.WIZARD
    power_source = PowerSourceEnum.ARCANE
    hit_points_per_level = 6
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        history=5, diplomacy=5, dungeoneering=5, nature=5, insight=5, religion=5
    )
    will = 2


class DruidClass(NPCClass):
    slug = NPCClassIntEnum.DRUID
    power_source = PowerSourceEnum.PRIMAL
    mandatory_skills = Skills(nature=5)
    trainable_skills = Skills(
        athletics=5,
        perception=5,
        endurance=5,
        history=5,
        arcana=5,
        diplomacy=5,
        insight=5,
        heal=5,
    )
    reflex = 1
    will = 1


class PriestClass(NPCClass):
    slug = NPCClassIntEnum.PRIEST
    power_source = PowerSourceEnum.DIVINE
    mandatory_skills = Skills(religion=5)
    trainable_skills = Skills(history=5, arcana=5, diplomacy=5, insight=5, heal=5)
    will = 2


class SeekerClass(NPCClass):
    slug = NPCClassIntEnum.SEEKER
    power_source = PowerSourceEnum.PRIMAL


class AvengerClass(NPCClass):
    slug = NPCClassIntEnum.AVENGER
    power_source = PowerSourceEnum.DIVINE
    mandatory_skills = Skills(religion=5)
    trainable_skills = Skills(
        acrobatics=5,
        athletics=5,
        perception=5,
        endurance=5,
        intimidate=5,
        streetwise=5,
        stealth=5,
        heal=5,
    )
    fortitude = 1
    reflex = 1
    will = 1


class WarlockClass(NPCClass):
    slug = NPCClassIntEnum.WARLOCK
    power_source = PowerSourceEnum.ARCANE
    trainable_skills = Skills(
        thievery=5,
        intimidate=5,
        streetwise=5,
        history=5,
        arcana=5,
        bluff=5,
        insight=5,
        religion=5,
    )
    reflex = 1
    will = 1


class SwordmageClass(NPCClass):
    slug = NPCClassIntEnum.SWORDMAGE
    power_source = PowerSourceEnum.ARCANE
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, history=5, diplomacy=5, insight=5
    )
    will = 2


class PaladinClass(NPCClass):
    slug = NPCClassIntEnum.PALADIN
    power_source = PowerSourceEnum.DIVINE
    mandatory_skills = Skills(religion=5)
    trainable_skills = Skills(
        endurance=5, intimidate=5, history=5, diplomacy=5, insight=5, heal=5
    )
    fortitude = 1
    reflex = 1
    will = 1


class RogueClass(NPCClass):
    slug = NPCClassIntEnum.ROGUE
    power_source = PowerSourceEnum.MARTIAL
    mandatory_skills = Skills(thievery=5, stealth=5)
    trainable_skills = Skills(
        acrobatics=5,
        athletics=5,
        perception=5,
        intimidate=5,
        streetwise=5,
        bluff=5,
        dungeoneering=5,
        insight=5,
    )
    reflex = 2


class RunepriestClass(NPCClass):
    slug = NPCClassIntEnum.RUNEPRIEST
    power_source = PowerSourceEnum.DIVINE


class RangerClass(NPCClass):
    power_source = PowerSourceEnum.MARTIAL
    mandatory_skills = Skills(nature=5, dungeoneering=5)
    trainable_skills = Skills(
        acrobatics=5, athletics=5, perception=5, endurance=5, stealth=5, heal=5
    )
    fortitude = 1
    reflex = 1


class RangerMarksmanClass(RangerClass):
    slug = NPCClassIntEnum.RANGER_MARKSMAN


class RangerMeleeClass(RangerClass):
    slug = NPCClassIntEnum.RANGER_MELEE

    def hit_points_bonus(self, **kwargs):
        tier: int = kwargs.get('tier', 0)
        return tier * 5


class WardenClass(NPCClass):
    slug = NPCClassIntEnum.WARDEN
    power_source = PowerSourceEnum.PRIMAL
    mandatory_skills = Skills(nature=5)
    trainable_skills = Skills(
        athletics=5, perception=5, endurance=5, intimidate=5, dungeoneering=5, heal=5
    )
    hit_points_per_level = 10
    fortitude = 1
    will = 1


class SorcererClass(NPCClass):
    slug = NPCClassIntEnum.SORCERER
    power_source = PowerSourceEnum.ARCANE
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        athletics=5,
        endurance=5,
        intimidate=5,
        history=5,
        bluff=5,
        diplomacy=5,
        dungeoneering=5,
        nature=5,
        insight=5,
    )
    will = 2


class ShamanClass(NPCClass):
    slug = NPCClassIntEnum.SHAMAN
    power_source = PowerSourceEnum.PRIMAL
    mandatory_skills = Skills(nature=5)
    trainable_skills = Skills(
        athletics=5,
        perception=5,
        endurance=5,
        history=5,
        arcana=5,
        insight=5,
        religion=5,
        heal=5,
    )
    fortitude = 1
    will = 1
