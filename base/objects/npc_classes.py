from typing import ClassVar, Sequence, Union

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import (
    ArmorTypeIntEnum,
    NPCClassIntEnum,
    PowerSourceEnum,
    ShieldTypeEnum,
    SkillsEnum,
    WeaponCategoryIntEnum,
    WeaponHandednessEnum,
)
from base.objects.implement_types import (
    HolySymbol,
    ImplementType,
    KiFocus,
    Rod,
    Sphere,
    Totem,
    Wand,
)
from base.objects.skills import Skills
from base.objects.weapon_types import (
    AnnihilationBlade,
    Club,
    Dagger,
    ExquisiteAgonyScourge,
    HandCrossbow,
    Longspear,
    LongSword,
    Quaterstaff,
    RitualDagger,
    RitualSickle,
    Scimitar,
    ShortSword,
    Shuriken,
    Sling,
    Spear,
    UnarmedMonkStrile,
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

    def attack_bonus(self, weapon=None):
        level_bonus = self.npc._level_bonus + self.npc.half_level
        if weapon and self.npc.is_weapon_proficient(weapon=weapon):
            return level_bonus + weapon.prof_bonus
        return level_bonus

    @property
    def damage_bonus(self):
        return self.npc._level_bonus

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
    available_shield_types = (ShieldTypeEnum.LIGHT,)
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
    available_implement_types = (Wand, LongSword)
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
    available_implement_types = (KiFocus, HolySymbol)
    trainable_skills = Skills(
        acrobatics=5,
        arcana=5,
        athletics=5,
        bluff=5,
        diplomacy=5,
        history=5,
        intimidate=5,
        perception=5,
        religion=5,
        stealth=5,
        thievery=5,
    )

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
    hit_points_per_level = 10

    class SubclassEnum(IntDescriptionSubclassEnum):
        THANEBORN = 1, 'Глава клана'
        RAGEBLOOD = 2, 'Яростная кровь'
        THUNDERBORN = 3, 'Громорождённый'
        WHIRLING = 4, 'Крутящийся'

    @property
    def _is_armored_properly(self) -> bool:
        return not self.npc.shield and (not self.npc.armor or self.npc.armor.is_light)

    @property
    def armor_class_bonus(self):
        result = super().armor_class_bonus
        if self._is_armored_properly:
            result += self.npc._tier + 1
        return result

    @property
    def reflex(self):
        if self._is_armored_properly:
            return self.npc._tier + 1
        return 0


class WarlordClass(NPCClass):
    slug = NPCClassIntEnum.WARLORD
    power_source = PowerSourceEnum.MARTIAL
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_shield_types = (ShieldTypeEnum.LIGHT,)
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

    class SubclassEnum(IntDescriptionSubclassEnum):
        INSPIRING = 1, 'Вдохновитель'
        TACTICAL = 2, 'Тактик'


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
    available_shield_types = (ShieldTypeEnum.LIGHT, ShieldTypeEnum.HEAVY)
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
        # brawler fighter should have melee weapon in just one hand
        if any(
            (
                self.npc.subclass != self.SubclassEnum.BRAWLER,
                self.npc.shield,
                len(weapons := tuple(self.npc.weapons.all())) != 1,
                not weapons[0].weapon_type.data_instance.category.is_melee,
                weapons[0].weapon_type.data_instance.handedness
                == WeaponHandednessEnum.TWO,
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

    def attack_bonus(self, weapon=None):
        result = super(FighterClass, self).attack_bonus(weapon)
        if not weapon:
            return result
        if self.npc.subclass == self.SubclassEnum.GREAT_WEAPON:
            if (
                not self.npc.shield
                and weapon.weapon_type.data_instance.handedness
                != WeaponHandednessEnum.ONE
                and self.npc.weapons.count() == 1
            ):
                return result + 1
        if self.npc.subclass == self.SubclassEnum.GUARDIAN:
            if weapon.weapon_type.data_instance.handedness != WeaponHandednessEnum.TWO:
                return result + 1
        if self.npc.subclass == self.SubclassEnum.TEMPPEST:
            if (
                self.npc.weapons.count() == 2
                and weapon.weapon_type.data_instance.is_off_hand
            ):
                return result + 1
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

    class SubclassEnum(IntDescriptionSubclassEnum):
        WAND_OF_ACCURACY = 1, 'Меткость с волшебной палочкой'
        STAFF_OF_DEFENCT = 2, 'Защита с посохом'
        ORB_OF_IMPOSITION = 3, 'Наказание со сферой'
        # ORB_OF_DECEPTION = 4, ''
        # TOME_OF_BINDING = 5, ''
        # TOME_OF_READINESS = 6, ''


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

    @property
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
    available_implement_types = (Wand, Rod, RitualDagger, RitualSickle)
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

    class SubclassEnum(IntDescriptionSubclassEnum):
        FEY_PACT = 1, 'Фейский договор'
        INFERNAL_PACT = 2, 'Адский договор'
        STAR_PACT = 3, 'Звёздный договор'
        GLOOM_PACT = 4, 'Тёмный договор'
        ELEMENTAL_PACT = 5, 'Элементный договор'


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

    @property
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
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
        ArmorTypeIntEnum.SCALE,
        ArmorTypeIntEnum.PLATE,
    )
    available_shield_types = (ShieldTypeEnum.LIGHT, ShieldTypeEnum.HEAVY)
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

    def attack_bonus(self, weapon=None):
        if not weapon:
            return super().attack_bonus()
        base_bonus = super().attack_bonus(weapon=weapon)
        wt_data_instance = weapon.weapon_type.data_instance
        if type(wt_data_instance) in self.available_weapon_types and isinstance(
            wt_data_instance, Dagger
        ):
            return base_bonus + 1
        return base_bonus


class RunepriestClass(NPCClass):
    slug = NPCClassIntEnum.RUNEPRIEST
    power_source = PowerSourceEnum.DIVINE
    available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
        ArmorTypeIntEnum.SCALE,
    )
    available_shield_types = (ShieldTypeEnum.LIGHT,)

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

    @property
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
    available_shield_types = (ShieldTypeEnum.LIGHT, ShieldTypeEnum.HEAVY)
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
            return self.npc._level_bonus + self.npc.strength + 2 * self.npc._tier
        elif self.npc.subclass == self.SubclassEnum.WILD_MAGIC:
            return self.npc._level_bonus + self.npc.dexterity + 2 * self.npc._tier

    @property
    def _armor_class_ability_bonus(self):
        result = super()._armor_class_ability_bonus
        if self.npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
            result = max(self.npc.str_mod, result)
        return result

    @property
    def armor_class_bonus(self):
        if self.npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
            return max(self.npc.int_mod, self.npc.dex_mod, self.npc.str_mod)
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
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
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

    @property
    def available_armor_types(self):
        result = (
            ArmorTypeIntEnum.CLOTH,
            ArmorTypeIntEnum.LEATHER,
            ArmorTypeIntEnum.HIDE,
            ArmorTypeIntEnum.CHAINMAIL,
        )
        if self.npc.subclass in (
            self.SubclassEnum.INFERNAL_PACT,
            self.SubclassEnum.ELEMENTAL_PACT,
        ):
            result += (ArmorTypeIntEnum.SCALE,)
        return result

    @property
    def available_weapon_types(self):
        if self.npc.subclass == self.SubclassEnum.FEY_PACT:
            return (WinterMourningBlade,)
        if self.npc.subclass == self.SubclassEnum.INFERNAL_PACT:
            return (AnnihilationBlade,)
        if self.npc.subclass == self.SubclassEnum.GLOOM_PACT:
            return (ExquisiteAgonyScourge,)

    @property
    def damage_bonus(self):
        base_bonus = super().damage_bonus
        damage_modifier = 0
        if self.npc.subclass in (
            self.SubclassEnum.FEY_PACT,
            self.SubclassEnum.GLOOM_PACT,
        ):
            damage_modifier = self.npc.dex_mod
        if self.npc.subclass in (
            self.SubclassEnum.INFERNAL_PACT,
            self.SubclassEnum.ELEMENTAL_PACT,
        ):
            damage_modifier = self.npc.con_mod
        if self.npc.subclass == self.SubclassEnum.STAR_PACT:
            damage_modifier = self.npc.int_mod
        return base_bonus + (
            self.npc._level_bonus
            + ((self.npc.level - 5) // 10) * 2
            + 2
            + damage_modifier
        )


class MonkClass(NPCClass):
    slug = NPCClassIntEnum.MONK
    power_source: PowerSourceEnum.PSIONIC
    reflex = 1
    trainable_skills = Skills(
        acrobatics=5,
        athletics=5,
        perception=5,
        thievery=5,
        endurance=5,
        diplomacy=5,
        insight=5,
        religion=5,
        stealth=5,
        heal=5,
    )
    available_weapon_categories = ()
    available_accesories = (Quaterstaff, Club, Dagger, Spear, Sling, Shuriken)
    available_weapon_types = available_accesories + (UnarmedMonkStrile,)
    available_implement_types = available_accesories + (KiFocus,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        CENTERED_BREATH = 1, 'Сконцентрированное дыхание'
        STONE_FIST = 2, 'Каменный кулак'
        # IRON_SOUL = 3, 'Железная душа'
        # DESERT_WIND = 4, 'Пустнынный ветер'
        # ETERNAL_TIDE = 5, 'Вечный прилив'

    @property
    def fortitude(self):
        if self.npc.subclass == self.SubclassEnum.CENTERED_BREATH:
            return self.npc._tier + 2
        return 1

    @property
    def will(self):
        if self.npc.subclass == self.SubclassEnum.STONE_FIST:
            return self.npc._tier + 2
        return 1


class WarpriestClass(PriestClass):
    slug = NPCClassIntEnum.WARPRIEST
    power_source = PowerSourceEnum.DIVINE
    available_shield_types = (
        ShieldTypeEnum.LIGHT,
        ShieldTypeEnum.HEAVY,
    )
    available_implement_types = (HolySymbol,)
    fortitude = 1
    will = 1
