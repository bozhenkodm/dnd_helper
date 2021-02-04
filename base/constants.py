from enum import Enum
from functools import partial
from random import randint

from django.db import models

d4 = partial(randint, 1, 4)
d6 = partial(randint, 1, 6)
d8 = partial(randint, 1, 8)
d10 = partial(randint, 1, 10)
d12 = partial(randint, 1, 12)
d20 = partial(randint, 1, 20)
d100 = partial(randint, 1, 100)


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

    @property
    def lname(self):
        return self.name.lower()


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


class NPCRaceEnum(BaseCapitalizedEnum):
    DEVA = 'Дев'
    DOPPELGANGER = 'Доппельгангер'
    DRAGONBORN = 'Драконорожденный'
    DROW = 'Дроу'
    DUERGAR = 'Дуэргар'
    DWARF = 'Дварф'
    ELADRIN = 'Эладрин'
    ELF = 'Эльф'
    GITHZERAI = 'Гитзерай'
    GNOME = 'Гном'
    GNOLL = 'Гнолл'
    GOBLIN = 'Гоблин'
    GOLIATH = 'Голиаф'
    HALFELF = 'Полуэльф'
    HALFLING = 'Полурослик'
    HALFORC = 'Полуорк'
    HAMADRYAD = 'Гамадриада'
    HUMAN = 'Человек'
    KALASHTAR = 'Калаштар'
    KOBOLD = 'Кобольд'
    MINOTAUR = 'Минотавр'
    ORC = 'Орк'
    PIXIE = 'Пикси'
    TIEFLING = 'Тифлинг'
    TREANT = 'Древень'
    SATYR = 'Сатир'
    SHIFTER_RAZORCLAW = 'Шифтер, бритволапый'
    SHIFTER_LONGTEETH = 'Шифтер, длиннозубый'
    WARFORGED = 'Кованый'

    def is_shifter(self):
        return self in (self.SHIFTER_LONGTEETH, self.SHIFTER_RAZORCLAW)


class NPCClassEnum(BaseCapitalizedEnum):
    # TODO subtypes or different classes?
    AVENGER = 'Каратель'
    BARBARIAN = 'Варвар'
    BARD = 'Бард'
    DRUID = 'Друид'
    FIGHTER = 'Воин'
    INVOKER = 'Апостол'
    PALADIN = 'Паладин'
    PRIEST = 'Жрец'
    RANGER_MARKSMAN = 'Следопыт (Дальнобойный)'
    RANGER_MELEE = 'Следопыт (Рукопашник)'
    ROGUE = 'Плут'
    RUNEPRIEST_W = 'Рунный жрец (мстительный молот)'
    RUNEPRIEST_D = 'Рунный жрец (непокорное слово)'
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
    LIGHT = 'Лёгкий щит'
    HEAVY = 'Тяжелый щит'


class WeaponGroupEnum(BaseCapitalizedEnum):
    # Рукопашное
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
    # Дальнобойное
    SLING = 'Праща'
    CROSSBOW = 'Арбалет'
    BOW = 'Лук'


class WeaponCategoryEnum(BaseCapitalizedEnum):
    SIMPLE = 'Простое рукопашное'
    MILITARY = 'Воинское рукопашное'
    SUPERIOR = 'Превосходное рукопашное'
    SIMPLE_RANGED = 'Простое дальнобойное'
    MILITARY_RANGED = 'Воинское дальнобойное'
    SUPERIOR_RANGED = 'Превосходное дальнобойное'

    @property
    def is_melee(self):
        return self in (self.SIMPLE, self.MILITARY, self.SUPERIOR)


class DiceEnum(BaseCapitalizedEnum):
    D4 = 'k4'
    D6 = 'k6'
    D8 = 'k8'
    D10 = 'k10'
    D12 = 'k12'
    D20 = 'k20'
    D100 = 'k100'

    def roll(self, dice_number):
        dice_func = {
            self.D4: lambda: d4(),
            self.D6: lambda: d6(),
            self.D8: lambda: d8(),
            self.D10: lambda: d10(),
            self.D12: lambda: d12(),
            self.D20: lambda: d20(),
            self.D100: lambda: d100(),
        }[self]
        return sum(dice_func() for _ in range(dice_number))


class WeaponPropertyEnum(BaseCapitalizedEnum):
    VERSATILE = 'Универсальное'
    LIGHT_THROWN = 'Лёгкое метательное'
    OFF_HAND = 'Дополнительное'
    HEAVY_THROWN = 'Тяжелое метательное'
    HIGH_CRIT = 'Высококритичное'
    REACH = 'Досягаемость'

    LOAD_FREE = 'Зарядка свободным'
    LOAD_MINOR = 'Зарядка малым'
    SMALL = 'Маленький'


class WeaponHandednessEnum(BaseCapitalizedEnum):
    ONE = 'Одноручное'
    TWO = 'Двуручное'


class PowerSourceEnum(BaseCapitalizedEnum):
    MARTIAL = 'Воинский'
    DIVINE = 'Духовный'
    ARCANE = 'Магический'
    PRIMAL = 'Первородный'


class PowerFrequencyEnum(BaseCapitalizedEnum):
    PASSIVE = 'Пассивный'
    AT_WILL = 'Неограниченный'
    ENCOUNTER = 'На сцену'
    DAYLY = 'На день'


class PowerDamageTypeEnum(BaseCapitalizedEnum):
    NONE = ''
    ACID = 'Кислота'
    COLD = 'Холод'
    FIRE = 'Огонь'
    LIGHTNING = 'Электричество'
    NECROTIC = 'Некротическая энергия'
    POISON = 'Яд'
    PSYCHIC = 'Психическая энергия'
    RADIANT = 'Излучение'
    THUNDER = 'Звук'


class PowerEffectTypeEnum(BaseCapitalizedEnum):
    NONE = ''
    CHARM = 'Очарование'
    CONJURATION = 'Иллюзия'
    FEAR = 'Страх'
    HEALING = 'Исцеление'
    INVIGORATING = 'Укрепляющий'
    POISON = 'Яд'
    POLYMORPH = 'Превращение'
    RATTLING = 'Ужасающий'
    RELIABLE = 'Надежный'
    SLEEP = 'Сон'
    STANCE = 'Стойка'
    TELEPORTATION = 'Телепортация'
    ZONE = 'Зона'


class PowerActionTypeEnum(BaseCapitalizedEnum):
    STANDARD = 'Стандартное действие'
    MINOR = 'Малое действие'
    FREE = 'Свободное действие'
    MOVEMENT = 'Действие движения'
    PROVOKED = 'Провоцированное действие'
    INTERRUPT = 'Немедленное прерывание'
    REACTION = 'Немедленный ответ'
    NO_ACTION = 'Нет действия'


class AccessoryTypeEnum(BaseCapitalizedEnum):
    IMPLEMENT = 'Инструмент'
    WEAPON = 'Оружие'


class DefenceTypeEnum(BaseCapitalizedEnum):
    ARMOR_CLASS = 'КД'
    FORTITUDE = 'Стойкость'
    REFLEX = 'Реакция'
    WILL = 'Воля'


class PowerRangeTypeEnum(BaseCapitalizedEnum):
    MELEE_WEAPON = 'Рукопашное оружие'
    MELEE_DISTANCE = 'Рукопашное (дистанция)'
    MELEE_TOUCH = 'Рукопашное касание'
    PERSONAL = 'Персональный'
    RANGED_WEAPON = 'Дальнобойное оружие'
    RANGED_DISTANCE = 'Дальнобойное (дистанция)'
    RANGED_SIGHT = 'Дальнобойное (видимость)'
    CLOSE_BURST = 'Ближняя вспышка'
    CLOSE_BLAST = 'Ближняя волна'
    AREA_BURST = 'Зональная вспышка'
    AREA_WALL = 'Стена'

    @property
    def is_area(self):
        return self in (self.AREA_WALL, self.AREA_BURST)

    @property
    def is_melee(self):
        return self in (self.MELEE_DISTANCE, self.MELEE_TOUCH, self.MELEE_WEAPON)

    @property
    def is_close(self):
        return self in (self.CLOSE_BURST, self.CLOSE_BLAST)

    @property
    def is_ranged(self):
        return self in (self.RANGED_SIGHT, self.RANGED_WEAPON, self.RANGED_DISTANCE)

    @property
    def is_provokable(self):
        return self.is_ranged or self.is_area


print(
    '\n'.join(
        f'{item.upper()} = \'\''
        for item in '''

'''.split()
    )
)
