from typing import ClassVar, Sequence, Type

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import (
    AbilityEnum,
    ArmorTypeIntEnum,
    ClassRoleEnum,
    NPCClassEnum,
    PowerSourceEnum,
    ShieldTypeIntEnum,
    SkillEnum,
    WeaponCategoryIntEnum,
    WeaponHandednessEnum,
)
from base.helpers import modifier
from base.objects.skills import Skills
from base.objects.weapon_types import (
    AnnihilationBlade,
    Club,
    Dagger,
    ExquisiteAgonyScourge,
    HandCrossbow,
    HolySymbol,
    KiFocus,
    Longspear,
    LongSword,
    Quaterstaff,
    RitualDagger,
    RitualSickle,
    Rod,
    Scimitar,
    ShortSword,
    Shuriken,
    Sling,
    Spear,
    Sphere,
    Totem,
    UnarmedMonkStrile,
    Wand,
    WeaponType,
    WinterMourningBlade,
)


class NPCClass:
    slug: ClassVar[NPCClassEnum]
    power_source: ClassVar[PowerSourceEnum]
    role: ClassVar[ClassRoleEnum]
    _fortitude: ClassVar[int] = 0
    _reflex: ClassVar[int] = 0
    _will: ClassVar[int] = 0
    base_surges_per_day: ClassVar[int] = 6  # if level bonus is not applied
    base_attack_abilities: ClassVar[Sequence[AbilityEnum]] = ()
    mandatory_skills: ClassVar[Skills] = Skills()
    trainable_skills: ClassVar[Skills] = Skills()
    skill_bonuses: ClassVar[Skills] = Skills()
    _available_armor_types: ClassVar[Sequence[ArmorTypeIntEnum]] = (
        ArmorTypeIntEnum.CLOTH,
    )
    available_shield_types: ClassVar[Sequence[ShieldTypeIntEnum]] = ()
    available_weapon_categories: ClassVar[Sequence[WeaponCategoryIntEnum]] = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
    available_weapon_types: ClassVar[Sequence[Type[WeaponType]]] = ()
    available_implement_types: ClassVar[Sequence[Type[WeaponType]]] = ()
    hit_points_per_level_npc: ClassVar[int] = 8
    hit_points_per_level_pc: ClassVar[int] = 5

    class SubclassEnum(IntDescriptionSubclassEnum):
        pass

    def __init__(self, npc):
        self.npc = npc

    @property
    def hit_points_bonus(self) -> int:
        return 0

    @property
    def available_armor_types(self) -> Sequence[ArmorTypeIntEnum]:
        return self._available_armor_types

    def attack_bonus(self, weapon=None, is_implement: bool = False) -> int:
        level_bonus = self.npc._level_bonus + self.npc.half_level
        if weapon and not is_implement and self.npc.is_weapon_proficient(weapon=weapon):
            return level_bonus + weapon.prof_bonus
        return level_bonus

    @property
    def damage_bonus(self) -> int:
        return self.npc._level_bonus

    @property
    def _armor_class_ability_bonus(self) -> int:
        return max(map(modifier, (self.npc.intelligence, self.npc.dexterity)))

    @property
    def armor_class_bonus(self) -> int:
        result = 0
        if self.npc.armor:
            if self.npc.armor.armor_type in self.available_armor_types:
                result += self.npc.armor.armor_class
            result += self.npc.enhancement_with_magic_threshold(
                self.npc.armor.enchantment
            )
        if not self.npc.armor or self.npc.armor.is_light:
            result += self._armor_class_ability_bonus
        return result

    @property
    def fortitude(self) -> int:
        return self._fortitude

    @property
    def reflex(self) -> int:
        return self._reflex

    @property
    def will(self) -> int:
        return self._will


class InvokerClass(NPCClass):
    slug = NPCClassEnum.INVOKER
    power_source = PowerSourceEnum.DIVINE
    role = ClassRoleEnum.CONTROLLER
    _fortitude = 1
    _reflex = 1
    _will = 1
    mandatory_skills = Skills(religion=5)
    trainable_skills = Skills(
        endurance=5, history=5, intimidate=5, arcana=5, diplomacy=5, insight=5
    )
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_implement_types = (
        Rod,
        Quaterstaff,
    )
    hit_points_per_level_npc = 6
    hit_points_per_level_pc = 4
    base_attack_abilities = (AbilityEnum.WISDOM,)


class ArtificerClass(NPCClass):
    slug = NPCClassEnum.ARTIFICER
    power_source = PowerSourceEnum.ARCANE
    role = ClassRoleEnum.LEADER
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
    )
    available_implement_types = (Wand, Rod, Quaterstaff)
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        perception=5, thievery=5, history=5, diplomacy=5, dungeoneering=5, heal=5
    )
    _fortitude = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.INTELLIGENCE,)


class BardClass(NPCClass):
    slug = NPCClassEnum.BARD
    power_source = PowerSourceEnum.ARCANE
    role = ClassRoleEnum.LEADER
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_shield_types = (ShieldTypeIntEnum.LIGHT,)
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
    skill_bonuses = Skills.init_with_const(SkillEnum.sequence(), 1)
    _reflex = 1
    _will = 1
    base_surges_per_day = 7
    base_attack_abilities = (AbilityEnum.CHARISMA,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        CUNNING = 1, 'Хитрый'
        VALOROUS = 2, 'Доблестный'
        PRESCIENT = 3, 'Провидец'


class VampireClass(NPCClass):
    slug = NPCClassEnum.VAMPIRE
    power_source = PowerSourceEnum.SHADOW
    role = ClassRoleEnum.STRIKER
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
    base_surges_per_day = 2
    base_attack_abilities = (AbilityEnum.DEXTERITY, AbilityEnum.CHARISMA)

    @property
    def armor_class_bonus(self) -> int:
        result = super().armor_class_bonus
        if not self.npc.shield and (
            not self.npc.armor or self.npc.armor.armor_type == ArmorTypeIntEnum.CLOTH
        ):
            # Рефлексы вампира
            result += 2
        return result

    @property
    def damage_bonus(self) -> int:
        base_bonus = super().damage_bonus + self.npc.cha_mod
        if self.npc.level < 5:
            return base_bonus
        return base_bonus + (self.npc.level - 5) // 10 * 2 + 2


class BarbarianClass(NPCClass):
    slug = NPCClassEnum.BARBARIAN
    power_source = PowerSourceEnum.PRIMAL
    role = ClassRoleEnum.STRIKER
    _available_armor_types = (
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
    _fortitude = 2
    base_surges_per_day = 8
    hit_points_per_level_npc = 10
    hit_points_per_level_pc = 6
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        THANEBORN = 1, 'Глава клана'
        RAGEBLOOD = 2, 'Яростная кровь'
        THUNDERBORN = 3, 'Громорождённый'
        WHIRLING = 4, 'Крутящийся'

    @property
    def _is_armored_properly(self) -> bool:
        return not self.npc.shield and (not self.npc.armor or self.npc.armor.is_light)

    @property
    def armor_class_bonus(self) -> int:
        result = super().armor_class_bonus
        if self._is_armored_properly:
            result += self.npc._tier + 1
        return result

    @property
    def reflex(self) -> int:
        if self._is_armored_properly:
            return self.npc._tier + 1
        return 0


class WarlordClass(NPCClass):
    slug = NPCClassEnum.WARLORD
    power_source = PowerSourceEnum.MARTIAL
    role = ClassRoleEnum.LEADER
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_shield_types = (ShieldTypeIntEnum.LIGHT,)
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
    _fortitude = 1
    _will = 1
    base_surges_per_day = 7
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, history=5, diplomacy=5, heal=5
    )
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        INSPIRING = 1, 'Вдохновитель'
        TACTICAL = 2, 'Тактик'


class FighterClass(NPCClass):
    slug = NPCClassEnum.FIGHTER
    power_source = PowerSourceEnum.MARTIAL
    role = ClassRoleEnum.DEFENDER
    base_surges_per_day = 9
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
        ArmorTypeIntEnum.SCALE,
    )
    available_shield_types = (ShieldTypeIntEnum.LIGHT, ShieldTypeIntEnum.HEAVY)
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
        WeaponCategoryIntEnum.MILITARY_RANGED,
    )
    trainable_skills = Skills(
        athletics=5, endurance=5, intimidate=5, streetwise=5, heal=5
    )
    hit_points_per_level_pc = 6
    base_attack_abilities = (AbilityEnum.STRENGTH,)

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
                self.npc.secondary_hand,
                self.npc.primary_hand
                and not self.npc.primary_hand.data_instance.is_melee,
                self.npc.primary_hand
                and self.npc.primary_hand.data_instance.handedness
                == WeaponHandednessEnum.TWO,
            )
        ):
            return False
        return True

    @property
    def armor_class_bonus(self) -> int:
        result = super().armor_class_bonus
        if self._is_browler_and_properly_armed():
            result += 1
        return result

    @property
    def fortitude(self) -> int:
        result = 2  # base fighter fortitude bonus
        if self._is_browler_and_properly_armed():
            result += 2
        return result

    def attack_bonus(self, weapon=None, is_implement=False) -> int:
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
    slug = NPCClassEnum.WIZARD
    power_source = PowerSourceEnum.ARCANE
    role = ClassRoleEnum.CONTROLLER
    available_weapon_categories = []
    available_weapon_types = (Dagger, Quaterstaff)
    available_implement_types = (Wand, Sphere, Quaterstaff)
    hit_points_per_level_npc = 6
    hit_points_per_level_pc = 4
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        history=5, diplomacy=5, dungeoneering=5, nature=5, insight=5, religion=5
    )
    _will = 2
    base_attack_abilities = (AbilityEnum.INTELLIGENCE,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        WAND_OF_ACCURACY = 1, 'Меткость с волшебной палочкой'
        STAFF_OF_DEFENCT = 2, 'Защита с посохом'
        ORB_OF_IMPOSITION = 3, 'Наказание со сферой'
        # ORB_OF_DECEPTION = 4, ''
        # TOME_OF_BINDING = 5, ''
        # TOME_OF_READINESS = 6, ''


class DruidClass(NPCClass):
    slug = NPCClassEnum.DRUID
    power_source = PowerSourceEnum.PRIMAL
    role = ClassRoleEnum.CONTROLLER
    _available_armor_types = (
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
    _reflex = 1
    _will = 1
    base_surges_per_day = 7
    base_attack_abilities = (AbilityEnum.WISDOM,)


class PriestClass(NPCClass):
    slug = NPCClassEnum.PRIEST
    power_source = PowerSourceEnum.DIVINE
    role = ClassRoleEnum.LEADER
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
    )
    available_implement_types = (HolySymbol,)
    mandatory_skills = Skills(religion=5)
    trainable_skills = Skills(history=5, arcana=5, diplomacy=5, insight=5, heal=5)
    _will = 2
    base_surges_per_day = 7
    base_attack_abilities = (AbilityEnum.WISDOM,)


class SeekerClass(NPCClass):
    slug = NPCClassEnum.SEEKER
    power_source = PowerSourceEnum.PRIMAL
    role = ClassRoleEnum.CONTROLLER
    _available_armor_types = (ArmorTypeIntEnum.CLOTH, ArmorTypeIntEnum.LEATHER)
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
        WeaponCategoryIntEnum.MILITARY_RANGED,
    )
    mandatory_skills = Skills(nature=5)
    trainable_skills = Skills(
        acrobatics=5,
        athletics=5,
        endurance=5,
        heal=5,
        insight=5,
        intimidate=5,
        nature=5,
        perception=5,
        stealth=5,
    )
    _reflex = 1
    _will = 1
    base_surges_per_day = 7
    base_attack_abilities = (AbilityEnum.WISDOM,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        SPIRITBOND = 1, 'Духовная связь'
        BLOODBOND = 2, 'Кровавая связь'

    def attack_bonus(self, weapon=None, is_implement: bool = False) -> int:
        result = super().attack_bonus(weapon, is_implement)
        if self.npc.subclass == self.SubclassEnum.SPIRITBOND and (
            weapon.data_instance.thrown
        ):
            return result + 1
        return result

    @property
    def _armor_class_ability_bonus(self) -> int:
        result = super()._armor_class_ability_bonus
        if self.npc.subclass == self.SubclassEnum.SPIRITBOND:
            result = max(self.npc.str_mod, result)
        return result


class AvengerClass(NPCClass):
    slug = NPCClassEnum.AVENGER
    power_source = PowerSourceEnum.DIVINE
    role = ClassRoleEnum.STRIKER
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
    _fortitude = 1
    _reflex = 1
    _will = 1
    base_surges_per_day = 7
    base_attack_abilities = (AbilityEnum.WISDOM,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        PURSUIT = 1, 'Осуждение преследования'
        RETRIBUTION = 2, 'Осуждение расплаты'
        UNITY = 3, 'Осуждение единства'

    @property
    def armor_class_bonus(self) -> int:
        result = super().armor_class_bonus
        if not self.npc.shield and (
            not self.npc.armor or self.npc.armor.armor_type == ArmorTypeIntEnum.CLOTH
        ):
            result += 3
        return result


class WarlockClass(NPCClass):
    slug = NPCClassEnum.WARLOCK
    power_source = PowerSourceEnum.ARCANE
    role = ClassRoleEnum.STRIKER
    available_implement_types = (Wand, Rod, RitualDagger, RitualSickle)
    _available_armor_types = (
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
    _reflex = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.CHARISMA, AbilityEnum.CONSTITUTION)

    class SubclassEnum(IntDescriptionSubclassEnum):
        FEY_PACT = 1, 'Фейский договор'
        INFERNAL_PACT = 2, 'Адский договор'
        STAR_PACT = 3, 'Звёздный договор'
        GLOOM_PACT = 4, 'Тёмный договор'
        ELEMENTAL_PACT = 5, 'Элементный договор'


class SwordmageClass(NPCClass):
    slug = NPCClassEnum.SWORDMAGE
    power_source = PowerSourceEnum.ARCANE
    role = ClassRoleEnum.DEFENDER
    _available_armor_types = (
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
    _will = 2
    hit_points_per_level_pc = 6
    base_surges_per_day = 8
    base_attack_abilities = (AbilityEnum.INTELLIGENCE,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        ASSAULT_AEGIS = 1, 'Эгида атаки'
        SHIELDING_AEGIS = 2, 'Эгида защиты'
        ENSNAREMENT_AEGIS = 3, 'Эгида западни'

    @property
    def armor_class_bonus(self) -> int:
        result = super().armor_class_bonus
        if not self.npc.shield and not self.npc.secondary_hand:
            result += 3
        else:
            result += 1
        return result


class PaladinClass(NPCClass):
    slug = NPCClassEnum.PALADIN
    power_source = PowerSourceEnum.DIVINE
    role = ClassRoleEnum.DEFENDER
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
        ArmorTypeIntEnum.SCALE,
        ArmorTypeIntEnum.PLATE,
    )
    available_shield_types = (ShieldTypeIntEnum.LIGHT, ShieldTypeIntEnum.HEAVY)
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
    _fortitude = 1
    _reflex = 1
    _will = 1
    hit_points_per_level_pc = 6
    base_surges_per_day = 10
    base_attack_abilities = (AbilityEnum.STRENGTH, AbilityEnum.CHARISMA)


class RogueClass(NPCClass):
    slug = NPCClassEnum.ROGUE
    power_source = PowerSourceEnum.MARTIAL
    role = ClassRoleEnum.STRIKER
    _available_armor_types = (
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
    _reflex = 2
    base_attack_abilities = (AbilityEnum.DEXTERITY,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        DODGER = 1, 'Мастер уклонения'
        SCOUNDREL = 2, 'Жестокий головорез'
        RUFFAIN = 3, 'Верзила'
        SNEAK = 4, 'Скрытник'

    def attack_bonus(self, weapon=None, is_implement=False) -> int:
        if not weapon:
            return super().attack_bonus()
        base_bonus = super().attack_bonus(weapon=weapon)
        wt_data_instance = weapon.data_instance
        if type(wt_data_instance) in self.available_weapon_types and isinstance(
            wt_data_instance,
            (Dagger, Sling, HandCrossbow),  # should choose either dagger or ranged
        ):
            return base_bonus + 1
        return base_bonus


class RunepriestClass(NPCClass):
    slug = NPCClassEnum.RUNEPRIEST
    power_source = PowerSourceEnum.DIVINE
    role = ClassRoleEnum.LEADER
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
        ArmorTypeIntEnum.CHAINMAIL,
        ArmorTypeIntEnum.SCALE,
    )
    available_shield_types = (ShieldTypeIntEnum.LIGHT,)
    mandatory_skills = Skills(religion=5)
    trainable_skills = Skills(
        athletics=5,
        thievery=5,
        endurance=5,
        history=5,
        arcana=5,
        insight=5,
        heal=5,
    )
    _will = 2
    base_surges_per_day = 7
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        WRATHFUL_HAMMER = 1, 'Мстительный молот'
        DEFIANT_WORD = 2, 'Непокорное слово'


class RangerClass(NPCClass):
    slug = NPCClassEnum.RANGER
    power_source = PowerSourceEnum.MARTIAL
    role = ClassRoleEnum.STRIKER
    _available_armor_types = (
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
    _fortitude = 1
    _reflex = 1
    base_attack_abilities = (AbilityEnum.STRENGTH, AbilityEnum.DEXTERITY)

    class SubclassEnum(IntDescriptionSubclassEnum):
        MARKSMAN = 1, 'Стрелок'
        TWO_HANDED = 2, 'Обоерукий'

    @property
    def hit_points_bonus(self) -> int:
        if self.npc.subclass == self.SubclassEnum.TWO_HANDED:
            return (self.npc._tier + 1) * 5
        return 0


class WardenClass(NPCClass):
    slug = NPCClassEnum.WARDEN
    power_source = PowerSourceEnum.PRIMAL
    role = ClassRoleEnum.DEFENDER
    _available_armor_types = (
        ArmorTypeIntEnum.CLOTH,
        ArmorTypeIntEnum.LEATHER,
        ArmorTypeIntEnum.HIDE,
    )
    available_shield_types = (ShieldTypeIntEnum.LIGHT, ShieldTypeIntEnum.HEAVY)
    available_weapon_categories = (
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
    )
    mandatory_skills = Skills(nature=5)
    trainable_skills = Skills(
        athletics=5, perception=5, endurance=5, intimidate=5, dungeoneering=5, heal=5
    )
    hit_points_per_level_npc = 10
    hit_points_per_level_pc = 7
    _fortitude = 1
    _will = 1
    base_surges_per_day = 9
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        EARTHSTRENGTH = 1, 'Сила земли'
        WILDBLOOD = 2, 'Дикая кровь'


class SorcererClass(NPCClass):
    slug = NPCClassEnum.SORCERER
    power_source = PowerSourceEnum.ARCANE
    role = ClassRoleEnum.STRIKER
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
    _will = 2
    base_attack_abilities = (AbilityEnum.CHARISMA,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        DRAGON_MAGIC = 1, 'Драконья магия'
        WILD_MAGIC = 2, 'Дикая магия'

    @property
    def damage_bonus(self) -> int:
        if self.npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
            return self.npc._level_bonus + self.npc.str_mod + 2 * self.npc._tier
        elif self.npc.subclass == self.SubclassEnum.WILD_MAGIC:
            return self.npc._level_bonus + self.npc.dex_mod + 2 * self.npc._tier
        return 0

    @property
    def _armor_class_ability_bonus(self) -> int:
        result = super()._armor_class_ability_bonus
        if self.npc.subclass == self.SubclassEnum.DRAGON_MAGIC:
            result = max(self.npc.str_mod, result)
        return result


class ShamanClass(NPCClass):
    slug = NPCClassEnum.SHAMAN
    power_source = PowerSourceEnum.PRIMAL
    role = ClassRoleEnum.LEADER
    _available_armor_types = (
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
    _fortitude = 1
    _will = 1
    base_surges_per_day = 7
    base_attack_abilities = (AbilityEnum.WISDOM,)


class HexbladeClass(WarlockClass):
    slug = NPCClassEnum.HEXBLADE
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
    _fortitude = 1
    _reflex = 0
    _will = 1
    base_attack_abilities = (AbilityEnum.CHARISMA,)  # type: ignore

    @property
    def available_armor_types(self) -> Sequence[ArmorTypeIntEnum]:
        result = [
            ArmorTypeIntEnum.CLOTH,
            ArmorTypeIntEnum.LEATHER,
            ArmorTypeIntEnum.HIDE,
            ArmorTypeIntEnum.CHAINMAIL,
        ]
        if self.npc.subclass in (
            self.SubclassEnum.INFERNAL_PACT,
            self.SubclassEnum.ELEMENTAL_PACT,
        ):
            result.append(ArmorTypeIntEnum.SCALE)
        return result

    @available_armor_types.setter
    def available_armor_types(self, value):
        pass

    @property
    def available_weapon_types(self) -> Sequence[Type[WeaponType]]:
        if self.npc.subclass == self.SubclassEnum.FEY_PACT:
            return (WinterMourningBlade,)
        if self.npc.subclass == self.SubclassEnum.INFERNAL_PACT:
            return (AnnihilationBlade,)
        if self.npc.subclass == self.SubclassEnum.GLOOM_PACT:
            return (ExquisiteAgonyScourge,)
        return ()

    @available_weapon_types.setter
    def available_weapon_types(self, value):
        pass

    @property
    def damage_bonus(self) -> int:
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
        return base_bonus + (+((self.npc.level - 5) // 10) * 2 + 2 + damage_modifier)


class MonkClass(NPCClass):
    slug = NPCClassEnum.MONK
    power_source = PowerSourceEnum.PSIONIC
    role = ClassRoleEnum.STRIKER
    _reflex = 1
    base_surges_per_day = 7
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
    base_attack_abilities = (AbilityEnum.DEXTERITY,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        CENTERED_BREATH = 1, 'Сконцентрированное дыхание'
        STONE_FIST = 2, 'Каменный кулак'
        # IRON_SOUL = 3, 'Железная душа'
        # DESERT_WIND = 4, 'Пустнынный ветер'
        # ETERNAL_TIDE = 5, 'Вечный прилив'

    @property
    def fortitude(self) -> int:
        if self.npc.subclass == self.SubclassEnum.CENTERED_BREATH:
            return self.npc._tier + 2
        return 1

    @property
    def will(self) -> int:
        if self.npc.subclass == self.SubclassEnum.STONE_FIST:
            return self.npc._tier + 2
        return 1


class BladeSingerClass(WizardClass):
    slug = NPCClassEnum.BLADESINGER
    power_source = PowerSourceEnum.ARCANE
    role = ClassRoleEnum.CONTROLLER
    _available_armor_types = (ArmorTypeIntEnum.CLOTH, ArmorTypeIntEnum.LEATHER)
    available_weapon_categories = [
        WeaponCategoryIntEnum.SIMPLE,
        WeaponCategoryIntEnum.SIMPLE_RANGED,
        WeaponCategoryIntEnum.MILITARY,
        WeaponCategoryIntEnum.MILITARY_RANGED,
    ]
    available_implement_types = (Wand, Sphere, Quaterstaff)

    hit_points_per_level_npc = 6
    mandatory_skills = Skills(arcana=5)
    trainable_skills = Skills(
        acrobatics=5,
        athletics=5,
        intimidate=5,
        history=5,
        diplomacy=5,
        nature=5,
        perception=5,
    )
    _will = 2
    base_attack_abilities = (AbilityEnum.INTELLIGENCE,)
