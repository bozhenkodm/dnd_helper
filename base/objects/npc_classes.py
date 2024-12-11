from typing import ClassVar, Sequence

from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import AbilityEnum, NPCClassEnum, WeaponHandednessEnum


class NPCClass:
    slug: ClassVar[NPCClassEnum]
    _fortitude: ClassVar[int] = 0
    _reflex: ClassVar[int] = 0
    _will: ClassVar[int] = 0
    base_attack_abilities: ClassVar[Sequence[AbilityEnum]] = ()

    class SubclassEnum(IntDescriptionSubclassEnum):
        pass

    def __init__(self, npc):
        self.npc = npc

    def attack_bonus(self, weapon=None, is_implement: bool = False) -> int:
        level_bonus = self.npc._level_bonus + self.npc.half_level
        if weapon and not is_implement and self.npc.is_weapon_proficient(weapon=weapon):
            return level_bonus + weapon.prof_bonus
        return level_bonus

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
    _fortitude = 1
    _reflex = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.WISDOM,)


class ArtificerClass(NPCClass):
    slug = NPCClassEnum.ARTIFICER
    _fortitude = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.INTELLIGENCE,)


class BardClass(NPCClass):
    slug = NPCClassEnum.BARD
    _reflex = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.CHARISMA,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        CUNNING = 1, 'Хитрый'
        VALOROUS = 2, 'Доблестный'
        PRESCIENT = 3, 'Провидец'


class VampireClass(NPCClass):
    slug = NPCClassEnum.VAMPIRE
    base_attack_abilities = (AbilityEnum.DEXTERITY, AbilityEnum.CHARISMA)


class BarbarianClass(NPCClass):
    slug = NPCClassEnum.BARBARIAN
    _fortitude = 2
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
    def reflex(self) -> int:
        if self._is_armored_properly:
            return self.npc._tier + 1
        return 0


class WarlordClass(NPCClass):
    slug = NPCClassEnum.WARLORD
    _fortitude = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        INSPIRING = 1, 'Вдохновитель'
        TACTICAL = 2, 'Тактик'


class FighterClass(NPCClass):
    slug = NPCClassEnum.FIGHTER
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        GREAT_WEAPON = 1, 'Воин с большим оружием'
        GUARDIAN = 2, 'Воин защитник'
        BATTLERAGER = 3, 'Неистовый воин'
        TEMPPEST = 4, 'Воин вихрь'
        BRAWLER = 5, 'Воин задира'

    def _is_brawler_and_properly_armed(self) -> bool:
        # brawler fighter should have melee weapon in just one hand
        if any(
            (
                self.npc.subclass_instance
                and self.npc.subclass_instance.slug != 'BRAWLER',
                self.npc.shield,
                self.npc.secondary_hand,
                self.npc.primary_hand
                and not self.npc.primary_hand.weapon_type.is_melee,
                self.npc.primary_hand
                and self.npc.primary_hand.handedness == WeaponHandednessEnum.TWO,
            )
        ):
            return False
        return True

    @property
    def fortitude(self) -> int:
        result = 2  # base fighter fortitude bonus
        if self._is_brawler_and_properly_armed():
            result += 2
        return result

    def attack_bonus(self, weapon=None, is_implement=False) -> int:
        result = super(FighterClass, self).attack_bonus(weapon)
        if not weapon:
            return result
        if self.npc.subclass == self.SubclassEnum.GREAT_WEAPON:
            if (
                not self.npc.shield
                and weapon.weapon_type.handedness != WeaponHandednessEnum.ONE
                and bool(self.npc.primary_hand) != bool(self.npc.secondary_hand)  # xor
            ):
                return result + 1
        if self.npc.subclass == self.SubclassEnum.GUARDIAN:
            if weapon.weapon_type.handedness != WeaponHandednessEnum.TWO:
                return result + 1
        if self.npc.subclass == self.SubclassEnum.TEMPPEST:
            if (
                self.npc.primary_hand
                and self.npc.secondary_hand
                and weapon.weapon_type.is_off_hand
            ):
                return result + 1
        return result


class WizardClass(NPCClass):
    slug = NPCClassEnum.WIZARD
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
    _reflex = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.WISDOM,)


class PriestClass(NPCClass):
    slug = NPCClassEnum.PRIEST
    _will = 2
    base_attack_abilities = (AbilityEnum.WISDOM,)


class SeekerClass(NPCClass):
    slug = NPCClassEnum.SEEKER
    _reflex = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.WISDOM,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        SPIRITBOND = 1, 'Духовная связь'
        BLOODBOND = 2, 'Кровавая связь'

    def attack_bonus(self, weapon=None, is_implement: bool = False) -> int:
        result = super().attack_bonus(weapon, is_implement)
        if self.npc.subclass == self.SubclassEnum.SPIRITBOND and (
            weapon.weapon_type.thrown
        ):
            return result + 1
        return result


class AvengerClass(NPCClass):
    slug = NPCClassEnum.AVENGER
    _fortitude = 1
    _reflex = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.WISDOM,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        PURSUIT = 1, 'Осуждение преследования'
        RETRIBUTION = 2, 'Осуждение расплаты'
        UNITY = 3, 'Осуждение единства'


class WarlockClass(NPCClass):
    slug = NPCClassEnum.WARLOCK
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
    _will = 2
    base_attack_abilities = (AbilityEnum.INTELLIGENCE,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        ASSAULT_AEGIS = 1, 'Эгида атаки'
        SHIELDING_AEGIS = 2, 'Эгида защиты'
        ENSNAREMENT_AEGIS = 3, 'Эгида западни'


class PaladinClass(NPCClass):
    slug = NPCClassEnum.PALADIN
    _fortitude = 1
    _reflex = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.CHARISMA, AbilityEnum.STRENGTH)


class RogueClass(NPCClass):
    slug = NPCClassEnum.ROGUE
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
        if (
            weapon.weapon_type in self.npc.klass.weapon_types.all()
            or self.npc.subclass_instance
            and weapon.weapon_type in self.npc.subclass_instance.weapon_types.all()
            and weapon.weapon_type.slug in ('Dagger', 'Sling', 'HandCrossbow')
        ):  # should choose either dagger or ranged
            return base_bonus + 1
        return base_bonus


class RunepriestClass(NPCClass):
    slug = NPCClassEnum.RUNEPRIEST
    _will = 2
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        WRATHFUL_HAMMER = 1, 'Мстительный молот'
        DEFIANT_WORD = 2, 'Непокорное слово'


class RangerClass(NPCClass):
    slug = NPCClassEnum.RANGER
    _fortitude = 1
    _reflex = 1
    base_attack_abilities = (AbilityEnum.DEXTERITY, AbilityEnum.STRENGTH)

    class SubclassEnum(IntDescriptionSubclassEnum):
        MARKSMAN = 1, 'Стрелок'
        TWO_HANDED = 2, 'Обоерукий'


class WardenClass(NPCClass):
    slug = NPCClassEnum.WARDEN
    _fortitude = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.STRENGTH,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        EARTHSTRENGTH = 1, 'Сила земли'
        WILDBLOOD = 2, 'Дикая кровь'


class SorcererClass(NPCClass):
    slug = NPCClassEnum.SORCERER
    _will = 2
    base_attack_abilities = (AbilityEnum.CHARISMA,)

    class SubclassEnum(IntDescriptionSubclassEnum):
        DRAGON_MAGIC = 1, 'Драконья магия'
        WILD_MAGIC = 2, 'Дикая магия'


class ShamanClass(NPCClass):
    slug = NPCClassEnum.SHAMAN
    _fortitude = 1
    _will = 1
    base_attack_abilities = (AbilityEnum.WISDOM,)


class HexbladeClass(WarlockClass):
    slug = NPCClassEnum.HEXBLADE
    _fortitude = 1
    _reflex = 0
    _will = 1
    base_attack_abilities = (AbilityEnum.CHARISMA,)  # type: ignore


class MonkClass(NPCClass):
    slug = NPCClassEnum.MONK
    _reflex = 1
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
    _will = 2
    base_attack_abilities = (AbilityEnum.INTELLIGENCE,)
