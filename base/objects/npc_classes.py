from typing import ClassVar, Sequence, Union

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import (
    ArmorTypeIntEnum,
    NPCClassIntEnum,
    PowerSourceEnum,
    ShieldTypeEnum,
    SkillsEnum,
    WeaponCategoryIntEnum,
)
from base.objects.implement_types import (
    HolySymbol,
    ImplementType,
    Rod,
    Sphere,
    Totem,
    Wand, KiFocus,
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
    WinterMourningBlade,
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
    available_armor_types: ClassVar[Sequence[ArmorTypeIntEnum]] = (
        ArmorTypeIntEnum.CLOTH,
    )
    available_shield_types: ClassVar[Sequence[ShieldTypeEnum]] = ()
    available_weapon_categories: ClassVar[Sequence[WeaponCategoryIntEnum]] = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
    available_weapon_types: ClassVar[Sequence[WeaponType]] = ()
    available_implement_types: ClassVar[Sequence[Union[WeaponType, ImplementType]]] = ()
    hit_points_per_level: ClassVar[int] = 8

    # class SubclassEnum(IntDescriptionSubclassEnum):
    #     pass

    def __init__(self, npc):
        self.npc = npc

    @property
    def hit_points_bonus(self):
        return 0

    def attack_bonus(self, weapon):
        return 0

    @property
    def damage_bonus(self):
        return 0

    @staticmethod
    def _modifier(value: int) -> int:
        # TODO move to helper function for now it repeats logic in models
        return (value - 10) // 2

    @property
    def _armor_class_ability_bonus(self):
        return max(map(self._modifier, (self.npc.intelligence, self.npc.dexterity)))

    @property
    def armor_class_bonus(self):
        result = 0
        if self.npc.armor:
            if self.npc.armor.armor_type in self.available_armor_types:
                result += self.npc.armor.armor_class
            result += min(self.npc.armor.enchantment, self.npc._magic_threshold)
        if not self.npc.armor or self.npc.armor.is_light:
            result += self._armor_class_ability_bonus
        return result

    @property
    def fortitude_bonus(self):
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
    available_implement_types = (
        Rod,
        Quaterstaff,
    )
    hit_points_per_level = 6


class ArtificerClass(NPCClass):
    slug = NPCClassIntEnum.ARTIFICER
    power_source = PowerSourceEnum.ARCANE
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
    available_implement_types = (Wand, Rod, Quaterstaff)
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
    available_implement_types = (Wand,)
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
    available_implement_types = (KiFocus,HolySymbol)

    @property
    def armor_class_bonus(self):
        result = super().armor_class_bonus
        if not self.npc.shield and (
            not self.npc.armor or self.npc.armor.armor_type == ArmorTypeIntEnum.CLOTH
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

    @property
    def armor_class_bonus(self):
        result = super().armor_class_bonus
        if not self.npc.shield and (not self.npc.armor or self.npc.armor.is_light):
            result += self.npc._tier + 1
        return result

    @property
    def reflex(self):
        if not self.npc.shield and self.npc.armor and self.npc.armor.is_light:
            return self.npc._tier + 1


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
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, streetwise=5, heal=5
    )

    class SubclassEnum(IntDescriptionSubclassEnum):
        GREAT_WEAPON = 1, 'Воин с большим оружием'
        GUARDIAN = 2, 'Воин защитник'
        BATTLERAGER = 3, 'Неистовый воин'
        TEMPPEST = 4, 'Воин вихрь'
        BRAWLER = 5, 'Воин задира'

    def _is_browler_and_properly_armed(self) -> bool:
        # brawler fighter should have melee weaopn in just one hand
        if any(
            (
                self.npc.subclass != self.SubclassEnum.BRAWLER,
                self.npc.shield,
                len(weapons := tuple(self.npc.weapons.all())) != 1,
                not weapons[0].weapon_type.data_instance.category.is_melee,
            )
        ):
            return False
        return True

    @property
    def armor_class_bonus(self):
        result = super().armor_class_bonus
        if self._is_browler_and_properly_armed():
            result += 1
        return result

    @property
    def fortitude(self):
        # we are overriding class variable with method...
        result = 2  # base fighter fortitude bonus
        if self._is_browler_and_properly_armed():
            result += 2
        return result


class WizardClass(NPCClass):
    slug = NPCClassIntEnum.WIZARD
    power_source = PowerSourceEnum.ARCANE
    available_weapon_categories = ()
    available_weapon_types = (Dagger, Quaterstaff)
    available_implement_types = (Wand, Sphere, Quaterstaff)
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
    available_implement_types = (Totem,)
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
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_implement_types = (HolySymbol,)
    mandatory_skills = Skills(religion=5)
    trainable_skills = Skills(history=5, arcana=5, diplomacy=5, insight=5, heal=5)
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
    available_implement_types = (HolySymbol,)
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

    def armor_class_bonus(self):
        result = super().armor_class_bonus
        if not self.npc.shield and (
            not self.npc.armor or self.npc.armor.armor_type == ArmorTypeIntEnum.CLOTH
        ):
            result += 3
        return result


class WarlockClass(NPCClass):
    slug = NPCClassIntEnum.WARLOCK
    power_source = PowerSourceEnum.ARCANE
    available_implement_types = (Wand, Rod)
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
    available_implement_types = available_weapon_types
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, history=5, diplomacy=5, insight=5
    )
    will = 2

    def armor_class_bonus(self):
        result = super().armor_class_bonus
        # TODO add handling offhand weapon
        if not self.npc.shield:
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
    available_implement_types = (HolySymbol,)
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

    def attack_bonus(self, weapon):
        if not weapon:
            return 0
        wt_data_instance = weapon.weapon_type.data_instance
        if type(wt_data_instance) in self.available_weapon_types and isinstance(
            wt_data_instance, Dagger
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

    def hit_points_bonus(self):
        return (self.npc._tier + 1) * 5


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
    available_implement_types = (Dagger, Quaterstaff)
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

    @property
    def damage_bonus(self):
        if self.npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
            return self.npc.strength + 2 * self.npc._tier
        elif self.npc.subclass == self.SubclassEnum.WILD_MAGIC:
            return self.npc.dexterity + 2 * self.npc._tier

    @property
    def _armor_class_ability_bonus(self):
        result = super()._armor_class_ability_bonus
        if self.npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
            result = max(self._modifier(self.npc.strength), result)
        return result

    def armor_class_bonus(self):
        if self.npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
            return max(
                map(
                    self._modifier,
                    (self.npc.intelligence, self.npc.dexterity, self.npc.strength),
                )
            )
        return super().armor_class_bonus


class ShamanClass(NPCClass):
    slug = NPCClassIntEnum.SHAMAN
    power_source = PowerSourceEnum.PRIMAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
    available_weapon_categories = (WeaponCategoryIntEnum.SIMPLE,)
    available_weapon_types = (Longspear,)
    available_implement_types = (Totem,)
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


class HexbladeClass(WarlockClass):
    slug = NPCClassIntEnum.HEXBLADE
    power_source = PowerSourceEnum.ARCANE
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
    available_weapon_types = (WinterMourningBlade,)
    trainable_skills = Skills(
        thievery=5,
        intimidate=5,
        streetwise=5,
        stealth=5,
        history=5,
        arcana=5,
        bluff=5,
        insight=5,
        religion=5,
    )
    fortitude = 1
    reflex = 0
    will = 1

    class SubclassEnum(IntDescriptionSubclassEnum):
        FEY_PACT = 1, 'Фейский договор'

    @property
    def damage_bonus(self):
        return ((self.npc.level - 5) // 10) * 2 + 2 + self._modifier(self.npc.dexterity)
