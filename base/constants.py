from enum import Enum
from functools import partial
from random import randint

from django.db import models

d4 = partial(randint, 1, 4)
d6 = partial(randint, 1, 6)
d8 = partial(randint, 1, 8)
d10 = partial(randint, 1, 10)
d12 = partial(randint, 1, 12)


class BaseCapitalizedEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower().capitalize()

    @classmethod
    def generate_choices(cls, is_sorted=True):
        if is_sorted:
            return sorted(((item.name, item.value) for item in cls), key=lambda x: x[1])
        return ((item.name, item.value) for item in cls)

    @classmethod
    def generate_case(cls, field='name'):
        kwargs = ({field: item.name, 'then': models.Value(item.value)} for item in cls)
        whens = (models.When(**kws) for kws in kwargs)
        return models.Case(*whens, output_field=models.CharField())

    @classmethod
    def max_length(cls):
        return max(len(item.name) for item in cls)


class SexEnum(BaseCapitalizedEnum):
    M = 'Муж'
    F = 'Жен'
    N = 'Н/Д'


class AttributesEnum(BaseCapitalizedEnum):
    STRENGTH = 'Сила'
    CONSTITUTION = 'Телосложение'
    DEXTERITY = 'Ловкость'
    INTELLIGENCE = 'Интеллект'
    WISDOM = 'Мудрость'
    CHARISMA = 'Харизма'


class SizeEnum(BaseCapitalizedEnum):
    TINY = 'Крошечный'
    SMALL = 'Маленький'
    AVERAGE = 'Средний'
    BIG = 'Большой'
    LARGE = 'Огромный'


class VisionEnum(BaseCapitalizedEnum):
    NORMAL = 'Обычное'
    TWILIGHT = 'Сумеречное'
    DARK = 'Тёмное'


class NPCRace(BaseCapitalizedEnum):
    DEVA = 'Дев'
    DOPPELGANGER = 'Доппельгангер'
    DRAGONBORN = 'Драконорожденный'
    DROW = 'Дроу'
    DWARF = 'Дварф'
    ELADRIN = 'Эладрин'
    ELF = 'Эльф'
    GITHZERAI = 'Гитзерай'
    GNOME = 'Гном'
    GNOLL = 'Гнолл'
    GOBLIN = 'Гоблин'
    GOLIATH = 'Голиаф'
    HUMAN = 'Человек'
    HALFELF = 'Полуэльф'
    HALFLING = 'Полурослик'
    HALFORC = 'Полуорк'
    KALASHTAR = 'Калаштар'
    KOBOLD = 'Кобольд'
    MINOTAUR = 'Минотавр'
    ORC = 'Орк'
    TIEFLING = 'Тифлинг'
    TREANT = 'Древень'
    SHIFTER_RAZORCLAW = 'Шифтер, бритволапый'
    SHIFTER_LONGTEETH = 'Шифтер, длиннозубый'
    WARFORGED = 'Кованый'

    def is_shifter(self):
        return self in (self.SHIFTER_LONGTEETH, self.SHIFTER_RAZORCLAW)


class NPCClass(BaseCapitalizedEnum):
    AVENGER = 'Каратель'
    BARBARIAN = 'Варвар'
    BARD = 'Бард'
    DRUID = 'Друид'
    FIGHTER = 'Воин'
    INVOKER = 'Апостол'
    PALADIN = 'Паладин'
    PRIEST = 'Жрец'
    RANGER = 'Следопыт'
    ROGUE = 'Плут'
    SHAMAN = 'Шаман'
    SORCERER = 'Чародей'
    WARDEN = 'Хранитель'
    WARLORD = 'Военачальник'
    WARLOCK = 'Колдун'
    WIZARD = 'Волшебник'


class SkillsEnum(BaseCapitalizedEnum):
    ACROBATICS = 'Акробатика'
    ARCANA = 'Магия'
    ATHLETICS = 'Атлетика'
    BLUFF = 'Обман'
    DIPLOMACY = 'Переговоры'
    DUNGEONEERING = 'Подземелья'
    ENDURANCE = 'Выносливость'
    HEAL = 'Целительство'
    HISTORY = 'История'
    INSIGHT = 'Внимательность'
    INTIMIDATE = 'Запугивание'
    NATURE = 'Природа'
    PERCEPTION = 'Проницательность'
    RELIGION = 'Религия'
    STEALTH = 'Скрытность'
    STREETWISE = 'Знание улиц'
    THIEVERY = 'Воровство'

    def get_base_attribute(self):
        if self in (self.ACROBATICS, self.STEALTH, self.THIEVERY):
            return AttributesEnum.DEXTERITY
        if self in (self.ARCANA, self.HISTORY, self.RELIGION):
            return AttributesEnum.INTELLIGENCE
        if self == self.ATHLETICS:
            return AttributesEnum.STRENGTH
        if self in (self.BLUFF, self.DIPLOMACY, self.INTIMIDATE, self.STREETWISE):
            return AttributesEnum.CHARISMA
        if self in (
            self.DUNGEONEERING,
            self.HEAL,
            self.INSIGHT,
            self.NATURE,
            self.PERCEPTION,
        ):
            return AttributesEnum.WISDOM
        if self == self.ENDURANCE:
            return AttributesEnum.CONSTITUTION


class ArmorTypeEnum(BaseCapitalizedEnum):
    CLOTH = 'Тканевый'
    LEATHER = 'Кожаный'
    HIDE = 'Шкурный'
    CHAINMAIL = 'Кольчуга'
    SCALE = 'Чешуйчатый'
    PLATE = 'Латный'


class ShieldTypeEnum(BaseCapitalizedEnum):
    LIGHT = 'Лёгкий'
    HEAVY = 'Тяжелый'


class WeaponGroup(BaseCapitalizedEnum):
    AXE = 'Топор'
    MACE = 'Булава'
    LIGHT_BLADE = 'Лёгкий клинок'
    SPEAR = 'Копьё'
    STAFF = 'Посох'
    FLAIL = 'Цеп'
    HEAVY_BLADE = 'Тяжелый клинок'
    HAMMER = 'Молот'
    PICK = 'Кирка'
    POLEARM = 'Древковое'


class WeaponCategory(BaseCapitalizedEnum):
    SIMPLE = 'Простое'
    MILITARY = 'Воинское'
    SUPERIOR = 'Превосходное'


class DamageDice(Enum):
    D4 = ('1k4', lambda: d4())
    D6 = ('1k6', lambda: d6())
    D8 = ('1k8', lambda: d8())
    D10 = ('1k10', lambda: d10())
    D12 = ('1k12', lambda: d12())
    D2_4 = ('2k4', lambda: d4() + d4())
    D2_6 = ('2k6', lambda: d6() + d6())
    D2_8 = ('2k8', lambda: d8() + d8())
    D2_10 = ('2k10', lambda: d10() + d10())

    @classmethod
    def generate_choices(cls, is_sorted=True):
        if is_sorted:
            return sorted(((item.name, item.title) for item in cls), key=lambda x: x[1])
        return ((item.name, item.title) for item in cls)

    @property
    def title(self):
        return self.value[0]

    def roll(self):
        return self.value[1]()


class WeaponProperty(BaseCapitalizedEnum):
    VERSATILE = 'Универсальное'
    LIGHT_THROWN = 'Лёгкое метательное'
    OFF_HAND = 'Дополнительное'
    HEAVY_THROWN = 'Тяжелое метательное'
    HIGH_CRIT = 'Высококритичное'
    REACH = 'Досягаемость'
