from dataclasses import dataclass
from typing import ClassVar, Sequence, Union

from base.constants.constants import (
    DiceIntEnum,
    WeaponCategoryIntEnum,
    WeaponGroupEnum,
    WeaponHandednessEnum,
)


@dataclass
class WeaponType:
    """
    Longsword, waraxe and so on.
    """

    group: ClassVar[Union[Sequence[WeaponGroupEnum], WeaponGroupEnum]]
    category: ClassVar[WeaponCategoryIntEnum]
    damage_dice: ClassVar[DiceIntEnum]
    handedness: ClassVar[WeaponHandednessEnum] = WeaponHandednessEnum.ONE
    name: ClassVar[str] = None
    prof_bonus: ClassVar[int] = 2
    dice_number: ClassVar[int] = 1
    range: ClassVar[int] = 0

    # properties
    brutal: ClassVar[int] = 0
    is_off_hand: ClassVar[bool] = False
    is_light_thrown: ClassVar[bool] = False
    is_heavy_thrown: ClassVar[bool] = False
    is_high_crit: ClassVar[bool] = False
    is_reach: ClassVar[bool] = False
    is_load_free: ClassVar[
        bool
    ] = False  # TODO make it one with next, or replace with enum
    is_load_minor: ClassVar[bool] = False
    is_small: ClassVar[bool] = False
    is_defensive: ClassVar[bool] = False

    @classmethod
    @property
    def slug(cls):
        return cls.__name__

    @classmethod
    @property
    def properties(cls) -> dict:
        return {
            'brutal': cls.brutal,
            'off_hand': cls.is_off_hand,
            'light_thrown': cls.is_light_thrown,
            'heavy_thrown': cls.is_heavy_thrown,
            'high_crit': cls.is_high_crit,
            'reach': cls.is_reach,
            'load_free': cls.is_load_free,
            'load_minor': cls.is_load_minor,
            'small': cls.is_small,
            'defensive': cls.is_defensive,
            'versatile': cls.handedness == WeaponHandednessEnum.VERSATILE,
        }

    @property
    def max_range(self):
        return self.range * 2

    def damage(self, weapon_number=1):
        return f'{self.dice_number*weapon_number}{self.damage_dice.description}'

    @classmethod
    def has_group(cls, group: WeaponGroupEnum) -> bool:
        if isinstance(cls.group, Sequence):
            return group in cls.group
        return group == cls.group


class ImplementType(WeaponType):
    name: ClassVar[str] = None
    slug: ClassVar[str] = None
    category = WeaponCategoryIntEnum.IMPLEMENT
    damage_dice = None
    handedness = WeaponHandednessEnum.ONE
    prof_bonus = 0
    range: ClassVar[int] = 0
    is_off_hand: ClassVar[bool] = True


class LongSword(WeaponType):
    name = 'Длинный меч'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D8
    handedness = WeaponHandednessEnum.VERSATILE
    prof_bonus = 3


class Club(WeaponType):
    name = 'Дубинка'
    group = WeaponGroupEnum.MACE
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D6


class Dagger(WeaponType):
    name = 'Кинжал'
    group = WeaponGroupEnum.LIGHT_BLADE
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D4
    prof_bonus = 3
    is_off_hand = True
    is_light_thrown = True
    range = 5


class Javelin(WeaponType):
    name = 'Метательное копьё'
    group = WeaponGroupEnum.SPEAR
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D6
    is_heavy_thrown = True
    range = 10


class LightMace(WeaponType):
    name = 'Лёгкая булава'
    group = WeaponGroupEnum.MACE
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D6
    is_off_hand = True
    is_small = True


class Mace(WeaponType):
    name = 'Булава'
    group = WeaponGroupEnum.MACE
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D8
    handedness = WeaponHandednessEnum.VERSATILE


class ShortSpear(WeaponType):
    name = 'Короткое копьё'
    group = WeaponGroupEnum.SPEAR
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D6
    is_light_thrown = True
    is_off_hand = True
    is_small = True
    range = 5


class Sickle(WeaponType):
    name = 'Серп'
    group = WeaponGroupEnum.LIGHT_BLADE
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D6
    is_off_hand = True


class Spear(WeaponType):
    name = 'Копьё'
    group = WeaponGroupEnum.SPEAR
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D8
    handedness = WeaponHandednessEnum.VERSATILE


class SpikedGauntlet(WeaponType):
    name = 'Шипованная рукавица'
    group = WeaponGroupEnum.UNARMED
    category = WeaponCategoryIntEnum.SIMPLE
    damage_dice = DiceIntEnum.D6
    is_off_hand = True


class Greatclub(WeaponType):
    name = 'Палица'
    group = WeaponGroupEnum.MACE
    category = WeaponCategoryIntEnum.SIMPLE
    handedness = WeaponHandednessEnum.TWO
    damage_dice = DiceIntEnum.D4
    dice_number = 2


class Morningstar(WeaponType):
    name = 'Моргенштерн'
    group = WeaponGroupEnum.MACE
    category = WeaponCategoryIntEnum.SIMPLE
    handedness = WeaponHandednessEnum.TWO
    damage_dice = DiceIntEnum.D10


class Quaterstaff(WeaponType):
    name = 'Посох'
    group = WeaponGroupEnum.STAFF
    category = WeaponCategoryIntEnum.SIMPLE
    handedness = WeaponHandednessEnum.TWO
    damage_dice = DiceIntEnum.D8


class Scythe(WeaponType):
    name = 'Коса'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.SIMPLE
    handedness = WeaponHandednessEnum.TWO
    damage_dice = DiceIntEnum.D4
    dice_number = 2


class Battleaxe(WeaponType):
    name = 'Боевой топор'
    group = WeaponGroupEnum.AXE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.VERSATILE


class Broadsword(WeaponType):
    name = 'Широкий меч'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.VERSATILE


class Flail(WeaponType):
    name = 'Цеп'
    group = WeaponGroupEnum.FLAIL
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.VERSATILE


class Handaxe(WeaponType):
    name = 'Ручной топор'
    group = WeaponGroupEnum.AXE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D6
    is_off_hand = True
    is_heavy_thrown = True
    range = 5


class Khopesh(WeaponType):
    name = 'Хопеш'
    group = (WeaponGroupEnum.AXE, WeaponGroupEnum.HEAVY_BLADE)
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D8
    brutal = 1
    handedness = WeaponHandednessEnum.VERSATILE


class LightWarPick(WeaponType):
    name = 'Лёгкая боевая кирка'
    group = WeaponGroupEnum.PICK
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D6
    is_high_crit = True
    is_off_hand = True
    is_small = True


class Rapier(WeaponType):
    name = 'Рапира'
    group = WeaponGroupEnum.LIGHT_BLADE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D8
    prof_bonus = 3


class Scimitar(WeaponType):
    name = 'Ятаган'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D8
    is_high_crit = True


class Scourge(WeaponType):
    name = 'Плеть'
    group = WeaponGroupEnum.FLAIL
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D8
    is_off_hand = True


class ShortSword(WeaponType):
    name = 'Короткий меч'
    group = WeaponGroupEnum.LIGHT_BLADE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D6
    is_off_hand = True
    prof_bonus = 3


class ThrowingHammer(WeaponType):
    name = 'Метательный молот'
    group = WeaponGroupEnum.HAMMER
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D6
    range = 5
    is_off_hand = True
    is_heavy_thrown = True


class Trident(WeaponType):
    name = 'Трезубец'
    group = WeaponGroupEnum.SPEAR
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D8
    range = 3
    is_heavy_thrown = True
    handedness = WeaponHandednessEnum.VERSATILE


class Warhammer(WeaponType):
    name = 'Боевой молот'
    group = WeaponGroupEnum.HAMMER
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.VERSATILE


class WarPick(WeaponType):
    name = 'Боевая кирка'
    group = WeaponGroupEnum.PICK
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D8
    handedness = WeaponHandednessEnum.VERSATILE
    is_high_crit = True
    is_small = True


class Falchion(WeaponType):
    name = 'Фальшион'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D4
    dice_number = 2
    prof_bonus = 3
    handedness = WeaponHandednessEnum.TWO
    is_high_crit = True


class Glaive(WeaponType):
    name = 'Глефа'
    group = (WeaponGroupEnum.HEAVY_BLADE, WeaponGroupEnum.POLEARM)
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D4
    dice_number = 2
    handedness = WeaponHandednessEnum.TWO
    is_reach = True


class HeavyFlail(WeaponType):
    name = 'Тяжелый цеп'
    group = WeaponGroupEnum.FLAIL
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D6
    dice_number = 2
    handedness = WeaponHandednessEnum.TWO


class Maul(WeaponType):
    name = 'Кувалда'
    group = WeaponGroupEnum.HAMMER
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D6
    dice_number = 2
    handedness = WeaponHandednessEnum.TWO


class Greatsword(WeaponType):
    name = 'Двуручный меч'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.TWO
    prof_bonus = 3


class Halberg(WeaponType):
    name = 'Алебарда'
    group = (WeaponGroupEnum.AXE, WeaponGroupEnum.POLEARM)
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.TWO
    is_reach = True


class Longspear(WeaponType):
    name = 'Длинное копьё'
    group = (WeaponGroupEnum.SPEAR, WeaponGroupEnum.POLEARM)
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.TWO
    is_reach = True


class Greataxe(WeaponType):
    name = 'Секира'
    group = WeaponGroupEnum.AXE
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D12
    handedness = WeaponHandednessEnum.TWO
    is_high_crit = True


class HeavyWarPick(WeaponType):
    name = 'Тяжелая кирка'
    group = WeaponGroupEnum.PICK
    category = WeaponCategoryIntEnum.MILITARY
    damage_dice = DiceIntEnum.D12
    handedness = WeaponHandednessEnum.TWO
    is_high_crit = True
    is_small = True


class BastardSword(WeaponType):
    name = 'Полуторный меч'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D10
    handedness = WeaponHandednessEnum.VERSATILE
    prof_bonus = 3


class Craghammer(WeaponType):
    name = 'Скальный молот'
    group = WeaponGroupEnum.HAMMER
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D10
    brutal = 2
    handedness = WeaponHandednessEnum.VERSATILE


class Katar(WeaponType):
    name = 'Катар'
    group = WeaponGroupEnum.LIGHT_BLADE
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D6
    prof_bonus = 3
    is_off_hand = True
    is_high_crit = True


class Kukri(Dagger):
    name = 'Кукри'
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D6
    brutal = 1
    is_light_thrown = False
    is_off_hand = True
    range = 0
    prof_bonus = 2


class ParryingDagger(Dagger):
    name = 'Защитный кинжал (сай)'
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D4
    is_light_thrown = False
    is_off_hand = True
    is_defensive = True
    range = 0
    prof_bonus = 2


class Tratnyr(WeaponType):
    name = 'Тратнир'
    group = WeaponGroupEnum.SPEAR
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D8
    handedness = WeaponHandednessEnum.VERSATILE
    is_heavy_thrown = True
    range = 10


class TrippleHeadedFlail(WeaponType):
    name = 'Тройной цеп'
    group = WeaponGroupEnum.FLAIL
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D10
    prof_bonus = 3
    handedness = WeaponHandednessEnum.VERSATILE


class Waraxe(WeaponType):
    name = 'Боевой топор'
    group = WeaponGroupEnum.AXE
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D12
    handedness = WeaponHandednessEnum.VERSATILE


class ExecutionAxe(WeaponType):
    name = 'Топор палача'
    group = WeaponGroupEnum.AXE
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D12
    brutal = 2
    is_high_crit = True


class Fullblade(WeaponType):
    name = 'Большой клинок'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D12
    prof_bonus = 3
    is_high_crit = True


class Greatspear(WeaponType):
    name = 'Большое копьё'
    group = (WeaponGroupEnum.SPEAR, WeaponGroupEnum.POLEARM)
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D10
    prof_bonus = 3
    is_reach = True


class Mordenkrad(WeaponType):
    name = 'Морденкрад'
    group = WeaponGroupEnum.HAMMER
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D6
    dice_number = 2
    brutal = 1


class SpikedChain(WeaponType):
    name = 'Шипованная цепь'
    group = WeaponGroupEnum.FLAIL
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D4
    dice_number = 2
    prof_bonus = 3
    is_reach = True


class HandCrossbow(WeaponType):
    name = 'Ручной арбалет'
    group = WeaponGroupEnum.CROSSBOW
    category = WeaponCategoryIntEnum.SIMPLE_RANGED
    damage_dice = DiceIntEnum.D6
    range = 10
    is_load_free = True


class Sling(WeaponType):
    name = 'Праща'
    group = WeaponGroupEnum.SLING
    category = WeaponCategoryIntEnum.SIMPLE_RANGED
    damage_dice = DiceIntEnum.D6
    range = 10
    is_load_free = True


class Crossbow(WeaponType):
    name = 'Арбалет'
    group = WeaponGroupEnum.CROSSBOW
    category = WeaponCategoryIntEnum.SIMPLE_RANGED
    damage_dice = DiceIntEnum.D8
    range = 15
    is_load_minor = True


class RepeatingCrossbow(WeaponType):
    name = 'Самозарядный арбалет'
    group = WeaponGroupEnum.CROSSBOW
    category = WeaponCategoryIntEnum.SIMPLE_RANGED
    damage_dice = DiceIntEnum.D8
    range = 10
    is_load_free = True


class Longbow(WeaponType):
    name = 'Длинный лук'
    group = WeaponGroupEnum.BOW
    category = WeaponCategoryIntEnum.MILITARY_RANGED
    damage_dice = DiceIntEnum.D10
    range = 20
    is_load_free = True


class Shortbow(WeaponType):
    name = 'Короткий лук'
    group = WeaponGroupEnum.BOW
    category = WeaponCategoryIntEnum.MILITARY_RANGED
    damage_dice = DiceIntEnum.D8
    range = 15
    is_load_free = True
    is_small = True


class Shuriken(WeaponType):
    name = 'Сюрикен'
    group = WeaponGroupEnum.LIGHT_BLADE
    category = WeaponCategoryIntEnum.SUPERIOR_RANGED
    damage_dice = DiceIntEnum.D4
    range = 6
    is_light_thrown = True
    prof_bonus = 3


class Greatbow(WeaponType):
    name = 'Большой лук'
    group = WeaponGroupEnum.BOW
    category = WeaponCategoryIntEnum.SUPERIOR_RANGED
    damage_dice = DiceIntEnum.D12
    is_load_free = True
    range = 25


class SuperiorCrossbow(WeaponType):
    name = 'Превосходный арбалет'
    group = WeaponGroupEnum.CROSSBOW
    category = WeaponCategoryIntEnum.SUPERIOR_RANGED
    damage_dice = DiceIntEnum.D10
    is_load_minor = True
    prof_bonus = 3
    range = 20


class WinterMourningBlade(WeaponType):
    name = 'Клинок зимней скорби (Оружие договора)'
    group = WeaponGroupEnum.LIGHT_BLADE
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D10
    prof_bonus = 3


class AnnihilationBlade(WeaponType):
    name = 'Клинок аннигиляции (Оружие договора)'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D12


class ExquisiteAgonyScourge(WeaponType):
    name = 'Бич изысканной агонии (Оружие договора)'
    group = WeaponGroupEnum.FLAIL
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D10
    is_reach = True


class ChaosBlade(WeaponType):
    name = 'Клинок хаоса (Оружие договора)'
    group = WeaponGroupEnum.HEAVY_BLADE
    category = WeaponCategoryIntEnum.SUPERIOR
    dice_number = 2
    damage_dice = DiceIntEnum.D4
    is_high_crit = True


class UnarmedMonkStrile(WeaponType):
    name = 'Безоружный удар монаха'
    group = WeaponGroupEnum.UNARMED
    category = WeaponCategoryIntEnum.SUPERIOR
    damage_dice = DiceIntEnum.D8
    prof_bonus = 3
    is_off_hand = True


class RitualDagger(Dagger):
    name = 'Ритуальный кинжал'


class RitualSickle(Sickle):
    name = 'Ритуальный серп'


# Double axe 	AV 	+2 	1d10/1d10  	Axe 	Double weapon, off-hand
# Double flail 	AV 	+2 	1d8/1d8 Flail 	Double weapon, defensive, off-hand
# Double sword 	AV 	+3 	1d6/1d6 Light blade 	Double weapon, defensive, off-hand
# Urgrosh 	AV 	+2 	1d12/1d6 Axe, spear 	Double weapon, defensive, off-hand


class KiFocus(ImplementType):
    name = 'Фокусировка ци'
    slug = 'ki_focus'


class Totem(ImplementType):
    name = 'Тотем'
    slug = 'totem'


class Wand(ImplementType):
    name = 'Волшебная палочка'
    slug = 'wand'


class Rod(ImplementType):
    name = 'Жезл'
    slug = 'rod'


class HolySymbol(ImplementType):
    name = 'Символ веры'
    slug = 'holy_symbol'


class Sphere(ImplementType):
    name = 'Сфера'
    slug = 'sphere'
