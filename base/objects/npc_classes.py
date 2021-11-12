from typing import ClassVar, Sequence

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import (
    ArmorTypeIntEnum,
    NPCClassIntEnum,
    PowerSourceEnum,
    ShieldTypeEnum,
    SkillsEnum,
    WeaponCategoryIntEnum,
)
from base.objects.skills import Skills
from base.objects.weapon_types import (
    Dagger,
    HandCrossbow,
    Longspear,
    LongSword,
    Quaterstaff,
    Scimitar,
    ShortSword,
    Shuriken,
    Sling,
    WeaponType,
)


class NPCClass:
    slug: ClassVar[NPCClassIntEnum] = None
    power_source: ClassVar[PowerSourceEnum]
    fortitude: ClassVar[int] = 0
    reflex: ClassVar[int] = 0
    will: ClassVar[int] = 0
    mandatory_skills: ClassVar[Skills] = Skills()
    trainable_skills: ClassVar[Skills] = Skills()
    skill_bonuses: ClassVar[Skills] = Skills()
    available_armor_types: ClassVar[Sequence[ArmorTypeIntEnum]] = (ArmorTypeIntEnum.CLOTH,)
    available_shield_types: ClassVar[Sequence[ShieldTypeEnum]] = ()
    available_weapon_categories: ClassVar[Sequence[WeaponCategoryIntEnum]] = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
    available_weapon_types: ClassVar[Sequence[WeaponType]]
    # available_implement_types
    hit_points_per_level: ClassVar[int] = 8

    # class SubclassEnum(IntDescriptionSubclassEnum):
    #     pass

    def hit_points_bonus(self, **kwargs):
        return 0

    def attack_bonus(self, **kwargs):
        return 0

    def damage_bonus(self, **kwargs):
        return 0

    def armor_class_bonus(self, **kwargs):
        if npc := kwargs.get('npc'):
            # TODO handle armor here?
            return max(map(npc._modifier, (npc.intelligence, npc.dexterity)))
        return 0


class InvokerClass(NPCClass):
    slug = NPCClassIntEnum.INVOKER
    power_source = PowerSourceEnum.DIVINE
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    hit_points_per_level = 6


class ArtificerClass(NPCClass):
    slug = NPCClassIntEnum.ARTIFICER
    power_source = PowerSourceEnum.ARCANE
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        perception=5, thievery=5, history=5, diplomacy=5, dungeoneering=5, heal=5
    )
    fortitude = 1
    will = 1


class BardClass(NPCClass):
    slug = NPCClassIntEnum.BARD
    power_source = PowerSourceEnum.ARCANE
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
        WeaponCategoryIntEnum.MILITARY_RANGED,
    )
    available_weapon_types = (
        LongSword,
        ShortSword,
        Scimitar,
    )
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

    def armor_class_bonus(self, **kwargs):
        result = super().armor_class_bonus(**kwargs)
        if npc := kwargs.get('npc'):
            if not npc.shield and (
                not npc.armor or npc.armor.armor_type == ArmorTypeIntEnum.CLOTH
            ):
                # Рефлексы вампира
                result += 2
        return result


class BarbarianClass(NPCClass):
    slug = NPCClassIntEnum.BARBARIAN
    power_source = PowerSourceEnum.PRIMAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
    )
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
    )
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

    def armor_class_bonus(self, **kwargs):
        result = super().armor_class_bonus(**kwargs)
        if npc := kwargs.get('npc'):
            if not npc.shield and (not npc.armor or npc.armor.is_light):
                result += npc._tier + 1
        return result


class WarlordClass(NPCClass):
    slug = NPCClassIntEnum.WARLORD
    power_source = PowerSourceEnum.MARTIAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
    fortitude = 1
    will = 1
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, history=5, diplomacy=5, heal=5
    )


class FighterClass(NPCClass):
    slug = NPCClassIntEnum.FIGHTER
    power_source = PowerSourceEnum.MARTIAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
        ArmorTypeIntEnum.SCALE,
    )
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
        WeaponCategoryIntEnum.MILITARY_RANGED,
    )
    fortitude = 2
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, streetwise=5, heal=5
    )

    class SubclassEnum(IntDescriptionSubclassEnum):
        GREAT_WEAPON = 1, 'Воин с большим оружием'
        GUARDIAN = 2, 'Воин защитник'
        BATTLERAGER = 3, 'Неистовый воин'
        TEMPPEST = 4, 'Воин вихрь'
        BRAWLER = 5, 'Воин задира'


class WizardClass(NPCClass):
    slug = NPCClassIntEnum.WIZARD
    power_source = PowerSourceEnum.ARCANE
    available_weapon_categories = ()
    available_weapon_types = (Dagger, Quaterstaff)
    hit_points_per_level = 6
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        history=5, diplomacy=5, dungeoneering=5, nature=5, insight=5, religion=5
    )
    will = 2


class DruidClass(NPCClass):
    slug = NPCClassIntEnum.DRUID
    power_source = PowerSourceEnum.PRIMAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
    )
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
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    will = 2


class SeekerClass(NPCClass):
    slug = NPCClassIntEnum.SEEKER
    power_source = PowerSourceEnum.PRIMAL

    class SubclassEnum(IntDescriptionSubclassEnum):
        SPIRITBOND = 1, 'Духовная связь'
        BLOODBOND = 2, 'Кровавая связь'


class AvengerClass(NPCClass):
    slug = NPCClassIntEnum.AVENGER
    power_source = PowerSourceEnum.DIVINE
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
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

    def armor_class_bonus(self, **kwargs):
        if npc := kwargs.get('npc'):
            if not npc.shield and (
                not npc.armor or npc.armor.armor_type == ArmorTypeIntEnum.CLOTH
            ):
                return 3
        return super().armor_class_bonus(**kwargs)


class WarlockClass(NPCClass):
    slug = NPCClassIntEnum.WARLOCK
    power_source = PowerSourceEnum.ARCANE
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
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
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
    available_weapon_types = (
        LongSword,
        ShortSword,
    )  # TODO Fill it up
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, history=5, diplomacy=5, insight=5
    )
    will = 2

    def armor_class_bonus(self, **kwargs):
        result = super().armor_class_bonus(**kwargs)
        if npc := kwargs.get('npc'):
            # TODO add handling offhand weapon
            if not npc.shield:
                result += 3
            else:
                result += 1
        return result


class PaladinClass(NPCClass):
    slug = NPCClassIntEnum.PALADIN
    power_source = PowerSourceEnum.DIVINE
    available_armor_types = ArmorTypeIntEnum
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
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
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
    available_weapon_categories = ()
    available_weapon_types = (Dagger, ShortSword, Sling, HandCrossbow, Shuriken)

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

    class SubclassEnum(IntDescriptionSubclassEnum):
        DODGER = 1, 'Мастер уклонения'
        SCOUNDREL = 2, 'Жестокий головорез'
        RUFFAIN = 3, 'Верзила'
        SNEAK = 4, 'Скрытник'

    def attack_bonus(self, **kwargs):
        weapon = kwargs.get('weapon')
        if not weapon:
            return 0
        data_instance = weapon.weapon_type.data_instance
        if type(data_instance) in self.available_weapon_types and isinstance(
            data_instance, Dagger
        ):
            return 1
        return 0


class RunepriestClass(NPCClass):
    slug = NPCClassIntEnum.RUNEPRIEST
    power_source = PowerSourceEnum.DIVINE

    class SubclassEnum(IntDescriptionSubclassEnum):
        WRATHFUL_HAMMER = 1, 'Мстительный молот'
        DEFIANT_WORD = 2, 'Непокорное слово'


class RangerClass(NPCClass):
    power_source = PowerSourceEnum.MARTIAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
    )
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
        WeaponCategoryIntEnum.MILITARY_RANGED,
    )
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
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
    )
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
    mandatory_skills = Skills(nature=5)
    trainable_skills = Skills(
        athletics=5, perception=5, endurance=5, intimidate=5, dungeoneering=5, heal=5
    )
    hit_points_per_level = 10
    fortitude = 1
    will = 1

    class SubclassEnum(IntDescriptionSubclassEnum):
        EARTHSTRENGTH = 1, 'Сила земли'
        WILDBLOOD = 2, 'Дикая кровь'


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

    class SubclassEnum(IntDescriptionSubclassEnum):
        DRAGON_MAGIC = 1, 'Драконья магия'
        WILD_MAGIC = 2, 'Дикая магия'

    def damage_bonus(self, **kwargs):
        if npc := kwargs.get('npc'):
            if npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
                return npc.strength + 2 * npc._tier
            elif npc.subclass == self.SubclassEnum.WILD_MAGIC:
                return npc.dexterity + 2 * npc._tier
        return 0

    def armor_class_bonus(self, **kwargs):
        if npc := kwargs.get('npc'):
            if npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
                return max(
                    map(npc._modifier, (npc.intelligence, npc.dexterity, npc.strength))
                )
            return super().armor_class_bonus(npc=npc)
        return 0


class ShamanClass(NPCClass):
    slug = NPCClassIntEnum.SHAMAN
    power_source = PowerSourceEnum.PRIMAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
    available_weapon_categories = (WeaponCategoryIntEnum.SIMPLE,)
    available_weapon_types = (Longspear,)
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
