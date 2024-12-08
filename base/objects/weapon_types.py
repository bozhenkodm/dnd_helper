from dataclasses import dataclass
from typing import ClassVar, Literal, Optional

from base.constants.constants import PowerActionTypeEnum

RangedLoadAction = Literal[PowerActionTypeEnum.FREE, PowerActionTypeEnum.MINOR]


@dataclass
class WeaponType:
    """
    Longsword, waraxe and so on.
    """

    name: ClassVar[str]

    # property shows if weapon is a magic item itself
    is_magic_item: ClassVar[bool] = False

    primary_end: ClassVar[Optional[type["WeaponType"]]] = None

    @classmethod
    def slug(cls):
        return cls.__name__


class ImplementType(WeaponType):
    name: ClassVar[str]

    @classmethod
    def slug(cls):
        snake_case = ''
        for i, char in enumerate(cls.__name__):
            if i > 0 and char.isupper():
                snake_case += '_' + char.lower()
            else:
                snake_case += char.lower()
        return snake_case


class LongSword(WeaponType):
    name = 'Длинный меч'


class Club(WeaponType):
    name = 'Дубинка'


class Dagger(WeaponType):
    name = 'Кинжал'


class Javelin(WeaponType):
    name = 'Метательное копьё'


class LightMace(WeaponType):
    name = 'Лёгкая булава'


class Mace(WeaponType):
    name = 'Булава'


class ShortSpear(WeaponType):
    name = 'Короткое копьё'


class Sickle(WeaponType):
    name = 'Серп'


class Spear(WeaponType):
    name = 'Копьё'


class SpikedGauntlet(WeaponType):
    name = 'Шипованная рукавица'


class Greatclub(WeaponType):
    name = 'Палица'


class Morningstar(WeaponType):
    name = 'Моргенштерн'


class Quaterstaff(WeaponType):
    name = 'Посох'


class Scythe(WeaponType):
    name = 'Коса'


class Battleaxe(WeaponType):
    name = 'Боевой топор'


class Broadsword(WeaponType):
    name = 'Широкий меч'


class Flail(WeaponType):
    name = 'Цеп'


class Handaxe(WeaponType):
    name = 'Ручной топор'


class Khopesh(WeaponType):
    name = 'Хопеш'


class LightWarPick(WeaponType):
    name = 'Лёгкая боевая кирка'


class Rapier(WeaponType):
    name = 'Рапира'


class Scimitar(WeaponType):
    name = 'Ятаган'


class Scourge(WeaponType):
    name = 'Плеть'


class ShortSword(WeaponType):
    name = 'Короткий меч'


class ThrowingHammer(WeaponType):
    name = 'Метательный молот'


class Trident(WeaponType):
    name = 'Трезубец'


class Warhammer(WeaponType):
    name = 'Боевой молот'


class WarPick(WeaponType):
    name = 'Боевая кирка'


class Falchion(WeaponType):
    name = 'Фальшион'


class Glaive(WeaponType):
    name = 'Глефа'


class HeavyFlail(WeaponType):
    name = 'Тяжелый цеп'


class Maul(WeaponType):
    name = 'Кувалда'


class Greatsword(WeaponType):
    name = 'Двуручный меч'


class Halberg(WeaponType):
    name = 'Алебарда'


class Longspear(WeaponType):
    name = 'Длинное копьё'


class Greataxe(WeaponType):
    name = 'Секира'


class HeavyWarPick(WeaponType):
    name = 'Тяжелая кирка'


class BastardSword(WeaponType):
    name = 'Полуторный меч'


class Craghammer(WeaponType):
    name = 'Скальный молот'


class Katar(WeaponType):
    name = 'Катар'


class Kukri(Dagger):
    name = 'Кукри'


class ParryingDagger(Dagger):
    name = 'Защитный кинжал (сай)'


class Tratnyr(WeaponType):
    name = 'Тратнир'


class TrippleHeadedFlail(WeaponType):
    name = 'Тройной цеп'


class Waraxe(WeaponType):
    name = 'Отличный боевой топор'


class ExecutionAxe(WeaponType):
    name = 'Топор палача'


class Fullblade(WeaponType):
    name = 'Большой клинок'


class Greatspear(WeaponType):
    name = 'Большое копьё'


class Mordenkrad(WeaponType):
    name = 'Морденкрад'


class SpikedChain(WeaponType):
    name = 'Шипованная цепь'


class HandCrossbow(WeaponType):
    name = 'Ручной арбалет'


class Sling(WeaponType):
    name = 'Праща'
    range = 10


class Crossbow(WeaponType):
    name = 'Арбалет'


class RepeatingCrossbow(WeaponType):
    name = 'Самозарядный арбалет'


class Longbow(WeaponType):
    name = 'Длинный лук'


class Shortbow(WeaponType):
    name = 'Короткий лук'
    range = 15


class Shuriken(WeaponType):
    name = 'Сюрикен'


class Greatbow(WeaponType):
    name = 'Большой лук'


class SuperiorCrossbow(WeaponType):
    name = 'Превосходный арбалет'


class WinterMourningBlade(WeaponType):
    name = 'Клинок зимней скорби (Оружие договора)'
    is_magic_item = True


class AnnihilationBlade(WeaponType):
    name = 'Клинок аннигиляции (Оружие договора)'
    is_magic_item = True


class ExquisiteAgonyScourge(WeaponType):
    name = 'Бич изысканной агонии (Оружие договора)'
    is_magic_item = True


class ChaosBlade(WeaponType):
    name = 'Клинок хаоса (Оружие договора)'
    is_magic_item = True


class UnarmedMonkStrike(WeaponType):
    name = 'Безоружный удар монаха'
    is_magic_item = True


class RitualDagger(Dagger):
    name = 'Ритуальный кинжал'
    is_magic_item = True


class RitualSickle(Sickle):
    name = 'Ритуальный серп'
    is_magic_item = True


class DoubleAxe(WeaponType):
    name = 'Двойной топор'


class DoubleAxeSecondEnd(WeaponType):
    name = 'Двойной топор (второй конец)'
    primary_end = DoubleAxe


class DoubleFlail(WeaponType):
    name = 'Двойной цеп'


class DoubleFlailSecondEnd(WeaponType):
    name = 'Двойной цеп (второй конец)'
    primary_end = DoubleFlail


class DoubleSword(WeaponType):
    name = 'Двойной меч'


class DoubleSwordSecondEnd(WeaponType):
    name = 'Двойной меч (второй конец)'
    primary_end = DoubleSword


class Urgrosh(WeaponType):
    name = 'Ургрош'


class UrgroshSecondEnd(WeaponType):
    name = 'Ургрош (второй конец)'
    primary_end = Urgrosh


class KiFocus(ImplementType):
    name = 'Фокусировка ци'


class Totem(ImplementType):
    name = 'Тотем'


class Wand(ImplementType):
    name = 'Волшебная палочка'


class Rod(ImplementType):
    name = 'Жезл'


class HolySymbol(ImplementType):
    name = 'Символ веры'


class Sphere(ImplementType):
    name = 'Сфера'
