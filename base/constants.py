from enum import Enum

from django.db import models


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
    GOLIATH = 'Голиаф'
    HUMAN = 'Человек'
    HALFELF = 'Полуэльф'
    HALFLING = 'Полурослик'
    HALFORC = 'Полуорк'
    KALASHTAR = 'Калаштар'
    MINOTAUR = 'Минотавр'
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
