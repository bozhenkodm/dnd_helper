from dataclasses import dataclass
from typing import ClassVar


@dataclass
class ImplementType:
    """
    wand, rod and so on
    """

    name: ClassVar[str] = None
    slug: ClassVar[str] = None


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


class Totem(ImplementType):
    name = 'Тотем'
    slug = 'totem'


class KiFocus(ImplementType):
    name = 'Фокусировка ци'
    slug = 'ki_focus'
