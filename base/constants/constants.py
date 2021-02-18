from random import randint

from base.constants.base import BaseCapitalizedEnum, IntDescriptionEnum


class SexEnum(BaseCapitalizedEnum):
    M = 'Муж'
    F = 'Жен'
    N = 'Н/Д'


class AttributeEnum(BaseCapitalizedEnum):
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
    BUGBEAR = 'Багбир'
    VRYLOKA = 'Врылока'
    HAMADRYAD = 'Гамадриада'
    GITHZERAI = 'Гитзерай'
    GNOME = 'Гном'
    GNOLL = 'Гнолл'
    GOBLIN = 'Гоблин'
    GOLIATH = 'Голиаф'
    DWARF = 'Дварф'
    DEVA = 'Дев'
    GENASI_EARTHSOUL = 'Дженази, земля'
    GENASI_FIRESOUL = 'Дженази, огонь'
    GENASI_STORMSOUL = 'Дженази, шторм'
    GENASI_WATERSOUL = 'Дженази, вода'
    GENASI_WINDSOUL = 'Дженази, ветер'
    WILDEN = 'Дикарь'
    DOPPELGANGER = 'Доппельгангер'
    DRAGONBORN = 'Драконорожденный'
    DROW = 'Дроу'
    DUERGAR = 'Дуэргар'
    KALASHTAR = 'Калаштар'
    KENKU = 'Кенку'
    KOBOLD = 'Кобольд'
    WARFORGED = 'Кованый'
    BLADELING = 'Лезвие'
    MINOTAUR = 'Минотавр'
    MUL = 'Мул'
    ORC = 'Орк'
    HALFELF = 'Полуэльф'
    HALFLING = 'Полурослик'
    HALFORC = 'Полуорк'
    PIXIE = 'Пикси'
    SATYR = 'Сатир'
    TIEFLING = 'Тифлинг'
    THRI_KREEN = 'Три-крин'
    HOBGOBLIN = 'Хобгоблин'
    HUMAN = 'Человек'
    SHADAR_KAI = 'Шадар-Кай'
    SHIFTER_RAZORCLAW = 'Шифтер, бритволапый'
    SHIFTER_LONGTEETH = 'Шифтер, длиннозубый'
    ELADRIN = 'Эладрин'
    ELF = 'Эльф'

    def is_shifter(self):
        return self in (self.SHIFTER_LONGTEETH, self.SHIFTER_RAZORCLAW)


class NPCClassIntEnum(IntDescriptionEnum):
    INVOKER = 10, 'Апостол'
    ARTIFICER = 20, 'Артефактор'
    BARD = 30, 'Бард'
    BARBARIAN = 40, 'Варвар'
    WARLORD = 50, 'Военачальник'
    FIGHTER = 60, 'Воин'
    WIZARD = 70, 'Волшебник'
    DRUID = 80, 'Друид'
    PRIEST = 90, 'Жрец'
    SEEKER = 95, 'Ловчий'
    AVENGER = 100, 'Каратель'
    WARLOCK = 110, 'Колдун'
    SWORDMAGE = 120, 'Мечник-маг'
    PALADIN = 130, 'Паладин'
    ROGUE = 140, 'Плут'
    RUNEPRIEST = 150, 'Рунный жрец'
    RANGER_MARKSMAN = 160, 'Следопыт (Дальнобойный)'
    RANGER_MELEE = 170, 'Следопыт (Рукопашник)'
    WARDEN = 180, 'Хранитель'
    SORCERER = 190, 'Чародей'
    SHAMAN = 200, 'Шаман'


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
            return AttributeEnum.DEXTERITY
        if self in (self.ARCANA, self.HISTORY, self.RELIGION):
            return AttributeEnum.INTELLIGENCE
        if self == self.ATHLETICS:
            return AttributeEnum.STRENGTH
        if self in (self.BLUFF, self.DIPLOMACY, self.INTIMIDATE, self.STREETWISE):
            return AttributeEnum.CHARISMA
        if self in (
            self.DUNGEONEERING,
            self.HEAL,
            self.INSIGHT,
            self.NATURE,
            self.PERCEPTION,
        ):
            return AttributeEnum.WISDOM
        if self == self.ENDURANCE:
            return AttributeEnum.CONSTITUTION


class ArmorTypeIntEnum(IntDescriptionEnum):
    CLOTH = 10, 'Тканевый'
    LEATHER = 20, 'Кожаный'
    HIDE = 30, 'Шкурный'
    CHAINMAIL = 40, 'Кольчуга'
    SCALE = 50, 'Чешуйчатый'
    PLATE = 60, 'Латный'


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


class WeaponCategoryIntEnum(IntDescriptionEnum):
    SIMPLE = 1, 'Простое рукопашное'
    MILITARY = 2, 'Воинское рукопашное'
    SUPERIOR = 3, 'Превосходное рукопашное'
    SIMPLE_RANGED = 4, 'Простое дальнобойное'
    MILITARY_RANGED = 5, 'Воинское дальнобойное'
    SUPERIOR_RANGED = 6, 'Превосходное дальнобойное'

    @property
    def is_melee(self):
        return self in (self.SIMPLE, self.MILITARY, self.SUPERIOR)


class DiceIntEnum(IntDescriptionEnum):
    D4 = 4, 'k4'
    D6 = 6, 'k6'
    D8 = 8, 'k8'
    D10 = 10, 'k10'
    D12 = 12, 'k12'
    D20 = 20, 'k20'
    D100 = 100, 'k100'

    def roll(self, dice_number=1):
        return sum(randint(1, self) for _ in range(dice_number))


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
    MELEE_RANGED_WEAPON = 'Рукопашное или дальнобойное оружие'
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
        return self in (
            self.MELEE_DISTANCE,
            self.MELEE_TOUCH,
            self.MELEE_WEAPON,
            self.MELEE_RANGED_WEAPON,
        )

    @property
    def is_close(self):
        return self in (self.CLOSE_BURST, self.CLOSE_BLAST)

    @property
    def is_ranged(self):
        return self in (
            self.RANGED_SIGHT,
            self.RANGED_WEAPON,
            self.RANGED_DISTANCE,
            self.MELEE_RANGED_WEAPON,
        )

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
