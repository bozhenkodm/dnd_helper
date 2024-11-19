from enum import Enum, auto
from random import randint

from base.constants.base import BaseNameValueDescriptionEnum, IntDescriptionEnum


class SexEnum(BaseNameValueDescriptionEnum):
    M = auto(), 'Муж'
    F = auto(), 'Жен'
    N = auto(), 'Н/Д'


class AbilityEnum(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    STRENGTH = auto(), 'Сила'
    CONSTITUTION = auto(), 'Телосложение'
    DEXTERITY = auto(), 'Ловкость'
    INTELLIGENCE = auto(), 'Интеллект'
    WISDOM = auto(), 'Мудрость'
    CHARISMA = auto(), 'Харизма'


# noinspection PyArgumentList
class PowerVariables(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    STR = auto()
    CON = auto()
    DEX = auto()
    INT = auto()
    WIS = auto()
    CHA = auto()
    WPN = auto()  # weapon damage dice
    WPS = auto()  # secondary weapon damage dice
    LVL = auto()
    DMG = auto()  # damage bonus
    ATK = auto()  # attack bonus =
    # (class bonus + half level + level bonus + enhancement). NOT +POWER ATTACK BONUS
    EHT = auto()  # armament enhancement
    ITL = auto()  # item level


class SizeEnum(BaseNameValueDescriptionEnum):
    TINY = auto(), 'Крошечный'
    SMALL = auto(), 'Маленький'
    AVERAGE = auto(), 'Средний'
    BIG = auto(), 'Большой'
    LARGE = auto(), 'Огромный'


class VisionEnum(BaseNameValueDescriptionEnum):
    NORMAL = auto(), 'Обычное'
    TWILIGHT = auto(), 'Сумеречное'
    DARK = auto(), 'Тёмное'


class NPCRaceEnum(BaseNameValueDescriptionEnum):
    BUGBEAR = auto(), 'Багбир'
    VRYLOKA = auto(), 'Врылока'
    HAMADRYAD = auto(), 'Гамадриада'
    GITHZERAI = auto(), 'Гитзерай'
    GNOME = auto(), 'Гном'
    GNOLL = auto(), 'Гнолл'
    GOBLIN = auto(), 'Гоблин'
    GOLIATH = auto(), 'Голиаф'
    DWARF = auto(), 'Дварф'
    DEVA = auto(), 'Дев'
    GENASI_EARTHSOUL = auto(), 'Дженази, земля'
    GENASI_FIRESOUL = auto(), 'Дженази, огонь'
    GENASI_STORMSOUL = auto(), 'Дженази, шторм'
    GENASI_WATERSOUL = auto(), 'Дженази, вода'
    GENASI_WINDSOUL = auto(), 'Дженази, ветер'
    WILDEN = auto(), 'Дикарь'
    DOPPELGANGER = auto(), 'Доппельгангер'
    DRAGONBORN = auto(), 'Драконорожденный'
    DROW = auto(), 'Дроу'
    DUERGAR = auto(), 'Дуэргар'
    KALASHTAR = auto(), 'Калаштар'
    KENKU = auto(), 'Кенку'
    KOBOLD = auto(), 'Кобольд'
    WARFORGED = auto(), 'Кованый'
    BLADELING = auto(), 'Мечерождённый'
    MINOTAUR = auto(), 'Минотавр'
    MUL = auto(), 'Мул'
    ORC = auto(), 'Орк'
    HALFELF = auto(), 'Полуэльф'
    HALFLING = auto(), 'Полурослик'
    HALFORC = auto(), 'Полуорк'
    PIXIE = auto(), 'Пикси'
    SATYR = auto(), 'Сатир'
    TIEFLING = auto(), 'Тифлинг'
    THRI_KREEN = auto(), 'Три-крин'
    HOBGOBLIN = auto(), 'Хобгоблин'
    HUMAN = auto(), 'Человек'
    SHADAR_KAI = auto(), 'Шадар-Кай'
    SHIFTER_RAZORCLAW = auto(), 'Шифтер, бритволапый'
    SHIFTER_LONGTEETH = auto(), 'Шифтер, длиннозубый'
    ELADRIN = auto(), 'Эладрин'
    ELF = auto(), 'Эльф'


class NPCClassEnum(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    INVOKER = auto(), 'Апостол'
    ARTIFICER = auto(), 'Артефактор'
    BARD = auto(), 'Бард'
    BLADESINGER = auto(), 'Блэйдсингер'
    VAMPIRE = auto(), 'Вампир'
    BARBARIAN = auto(), 'Варвар'
    WARLORD = auto(), 'Военачальник'
    WARPRIEST = auto(), 'Военный священник (жрец)'
    FIGHTER = auto(), 'Воин'
    WIZARD = auto(), 'Волшебник'
    DRUID = auto(), 'Друид'
    PRIEST = auto(), 'Жрец'
    SEEKER = auto(), 'Ловчий'
    AVENGER = auto(), 'Каратель'
    WARLOCK = auto(), 'Колдун'
    SWORDMAGE = auto(), 'Мечник-маг'
    MONK = auto(), 'Монах'
    PALADIN = auto(), 'Паладин'
    ROGUE = auto(), 'Плут'
    RUNEPRIEST = auto(), 'Рунный жрец'
    RANGER = auto(), 'Следопыт'
    RANGER_MELEE = auto(), 'Следопыт (Рукопашник)'
    HEXBLADE = auto(), 'Хексблэйд (колдун)'
    WARDEN = auto(), 'Хранитель'
    SORCERER = auto(), 'Чародей'
    SHAMAN = auto(), 'Шаман'


class SkillEnum(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    ACROBATICS = auto(), 'Акробатика'
    ATHLETICS = auto(), 'Атлетика'
    PERCEPTION = auto(), 'Внимательность'
    THIEVERY = auto(), 'Воровство'
    ENDURANCE = auto(), 'Выносливость'
    INTIMIDATE = auto(), 'Запугивание'
    STREETWISE = auto(), 'Знание улиц'
    HISTORY = auto(), 'История'
    ARCANA = auto(), 'Магия'
    BLUFF = auto(), 'Обман'
    DIPLOMACY = auto(), 'Переговоры'
    DUNGEONEERING = auto(), 'Подземелья'
    NATURE = auto(), 'Природа'
    INSIGHT = auto(), 'Проницательность'
    RELIGION = auto(), 'Религия'
    STEALTH = auto(), 'Скрытность'
    HEAL = auto(), 'Целительство'

    @classmethod
    def sequence(cls):
        yield from cls

    def get_base_ability(self):
        if self in (self.ACROBATICS, self.STEALTH, self.THIEVERY):
            return AbilityEnum.DEXTERITY
        if self in (self.ARCANA, self.HISTORY, self.RELIGION):
            return AbilityEnum.INTELLIGENCE
        if self == self.ATHLETICS:
            return AbilityEnum.STRENGTH
        if self in (self.BLUFF, self.DIPLOMACY, self.INTIMIDATE, self.STREETWISE):
            return AbilityEnum.CHARISMA
        if self in (
            self.DUNGEONEERING,
            self.HEAL,
            self.INSIGHT,
            self.NATURE,
            self.PERCEPTION,
        ):
            return AbilityEnum.WISDOM
        if self == self.ENDURANCE:
            return AbilityEnum.CONSTITUTION


class ArmorTypeIntEnum(IntDescriptionEnum):
    CLOTH = 0, 'Тканевый'
    LEATHER = 2, 'Кожаный'
    HIDE = 3, 'Шкурный'
    CHAINMAIL = 6, 'Кольчуга'
    SCALE = 7, 'Чешуйчатый'
    PLATE = 8, 'Латный'


class ShieldTypeIntEnum(IntDescriptionEnum):
    NONE = 0, '----------'
    LIGHT = 1, 'Лёгкий щит'
    HEAVY = 2, 'Тяжелый щит'

    @property
    def skill_penalty(self):
        if self == self.HEAVY:
            return 2
        return 0

    @classmethod
    def get_by_value(cls, value) -> 'ShieldTypeIntEnum':
        for item in cls:
            if item.value == value:
                return item
        raise ValueError('Wrong shield')


class WeaponGroupEnum(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    # Melee
    AXE = auto(), 'Топор'
    MACE = auto(), 'Булава'
    LIGHT_BLADE = auto(), 'Лёгкий клинок'
    SPEAR = auto(), 'Копьё'
    STAFF = auto(), 'Посох'
    FLAIL = auto(), 'Цеп'
    HEAVY_BLADE = auto(), 'Тяжелый клинок'
    HAMMER = auto(), 'Молот'
    PICK = auto(), 'Кирка'
    POLEARM = auto(), 'Древковое'
    UNARMED = auto(), 'Безоружное'
    # Ranged
    SLING = auto(), 'Праща'
    CROSSBOW = auto(), 'Арбалет'
    BOW = auto(), 'Лук'


class WeaponCategoryIntEnum(IntDescriptionEnum):
    SIMPLE = 1, 'Простое рукопашное'
    MILITARY = 2, 'Воинское рукопашное'
    SUPERIOR = 3, 'Превосходное рукопашное'
    SIMPLE_RANGED = 4, 'Простое дальнобойное'
    MILITARY_RANGED = 5, 'Воинское дальнобойное'
    SUPERIOR_RANGED = 6, 'Превосходное дальнобойное'
    IMPLEMENT = 7, 'Инструмент'

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


class WeaponHandednessEnum(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    ONE = auto(), 'Одноручное'
    TWO = auto(), 'Двуручное'
    VERSATILE = (
        auto(),
        'Универсальное',
    )  # one-handed, but can be used with two hands
    # (with +1 to damage, unless user is small)
    FREE = auto(), 'Не занимает руки'  # ki and symbols of faith


class PowerSourceEnum(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    MARTIAL = auto(), 'Воинский'
    DIVINE = auto(), 'Духовный'
    ARCANE = auto(), 'Магический'
    PRIMAL = auto(), 'Первородный'
    SHADOW = auto(), 'Теневой'
    PSIONIC = auto(), 'Псионический'


class ClassRoleEnum(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    STRIKER = auto(), 'Атакующий'
    DEFENDER = auto(), 'Защитник'
    CONTROLLER = auto(), 'Контроллер'
    LEADER = auto(), 'Лидер'


class PowerFrequencyEnum(BaseNameValueDescriptionEnum):
    PASSIVE = auto(), 'Пассивный'
    AT_WILL = auto(), 'Неограниченный'
    ENCOUNTER = auto(), 'На сцену'
    DAILY = auto(), 'На день'


class PowerDamageTypeEnum(BaseNameValueDescriptionEnum):
    NONE = auto(), ''
    ACID = auto(), 'Кислота'
    COLD = auto(), 'Холод'
    FIRE = auto(), 'Огонь'
    LIGHTNING = auto(), 'Электричество'
    NECROTIC = auto(), 'Некротическая энергия'
    POISON = auto(), 'Яд'
    PSYCHIC = auto(), 'Психическая энергия'
    RADIANT = auto(), 'Излучение'
    THUNDER = auto(), 'Звук'
    FORCE = auto(), 'Силовое поле'


class PowerEffectTypeEnum(BaseNameValueDescriptionEnum):
    NONE = auto(), ''
    CHARM = auto(), 'Очарование'
    CONJURATION = auto(), 'Иллюзия'
    FEAR = auto(), 'Страх'
    HEALING = auto(), 'Исцеление'
    INVIGORATING = auto(), 'Укрепляющий'
    POLYMORPH = auto(), 'Превращение'
    RAGE = auto(), 'Ярость'
    RATTLING = auto(), 'Ужасающий'
    RELIABLE = auto(), 'Надежный'
    SLEEP = auto(), 'Сон'
    STANCE = auto(), 'Стойка'
    TELEPORTATION = auto(), 'Телепортация'
    ZONE = auto(), 'Зона'


class PowerActionTypeEnum(BaseNameValueDescriptionEnum):
    STANDARD = auto(), 'Стандартное действие'
    MINOR = auto(), 'Малое действие'
    FREE = auto(), 'Свободное действие'
    MOVEMENT = auto(), 'Действие движения'
    PROVOKED = auto(), 'Провоцированное действие'
    INTERRUPT = auto(), 'Немедленное прерывание'
    REACTION = auto(), 'Немедленный ответ'
    NO_ACTION = auto(), 'Нет действия'


class AccessoryTypeEnum(BaseNameValueDescriptionEnum):
    IMPLEMENT = auto(), 'Инструмент'
    WEAPON = auto(), 'Оружие'
    TWO_WEAPONS = auto(), 'Два оружия'
    # WEAPON_AND_IMPLEMENT = 'WEAPON_AND_IMPLEMENT', 'Оружие и инструмент'


class DefenceTypeEnum(BaseNameValueDescriptionEnum):
    ARMOR_CLASS = auto(), 'КД'
    FORTITUDE = auto(), 'Стойкость'
    REFLEX = auto(), 'Реакция'
    WILL = auto(), 'Воля'


class PowerRangeTypeEnum(BaseNameValueDescriptionEnum):
    MELEE_WEAPON = auto(), 'Рукопашное оружие'
    MELEE = auto(), 'Рукопашное'
    RANGED = auto(), 'Дальнобойное'
    MELEE_RANGED_WEAPON = auto(), 'Рукопашное или дальнобойное оружие'
    RANGED_WEAPON = auto(), 'Дальнобойное оружие'
    BURST = auto(), 'Вспышка'
    BLAST = auto(), 'Волна'
    WALL = auto(), 'Стена'
    PERSONAL = auto(), 'Персональный'

    def default_target(self):
        if self in (
            self.MELEE_WEAPON,
            self.MELEE,
            self.RANGED,
            self.MELEE_RANGED_WEAPON,
            self.RANGED_WEAPON,
        ):
            return 'Одно существо'
        if self == self.BURST:
            return 'Все существа во вспышке'
        if self == self.BLAST:
            return 'Все существа в волне'
        return '----------'

    @property
    def is_melee_weapon(self):
        return self in (self.MELEE_WEAPON, self.MELEE_RANGED_WEAPON)

    @property
    def is_ranged_weapon(self):
        return self in (self.RANGED_WEAPON, self.MELEE_RANGED_WEAPON)


class PowerPropertyTitle(BaseNameValueDescriptionEnum):
    ATTACK = auto(), 'Атака'
    HIT = auto(), 'Попадание'
    MISS = auto(), 'Промах'
    EFFECT = auto(), 'Эффект'
    REQUIREMENT = auto(), 'Требование'
    TRIGGER = auto(), 'Триггер'
    SPECIAL = auto(), 'Особенность'
    TARGET = auto(), 'Цель'
    OTHER = auto(), 'Другое'


class MagicItemCategory(BaseNameValueDescriptionEnum):
    COMMON = auto(), 'Обычный'
    UNCOMMON = auto(), 'Необычный'
    RARE = auto(), 'Редкий'


class MagicItemSlot(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    WEAPON = auto(), 'Оружие'
    ARMOR = auto(), 'Броня'
    NECK = auto(), 'Шея'
    HEAD = auto(), 'Голова'
    ARMS = auto(), 'Предплечья/Щит'
    FEET = auto(), 'Обувь'
    HANDS = auto(), 'Перчатки'
    WAIST = auto(), 'Пояс'
    RING = auto(), 'Кольца'
    WONDROUS_ITEMS = auto(), 'Чудесный предмет'
    TATOO = auto(), 'Татуировка'

    def is_simple(self) -> bool:
        return self not in (
            self.WEAPON,
            self.ARMOR,
            self.ARMS,
            self.NECK,
        )


class ThrownWeaponType(BaseNameValueDescriptionEnum):
    def _generate_next_value_(name, start, count, last_values):
        return str(name).lower()

    LIGHT = auto(), 'Лёгкое'
    HEAVY = auto(), 'Тяжёлое'


class BonusSource(BaseNameValueDescriptionEnum):
    CLASS = auto(), 'Бонус класса'
    RACE = auto(), 'Расовый бонус'
    POWER = auto(), 'Бонус таланта'
    FEAT = auto(), 'Бонус черты'
    ITEM = auto(), 'Бонус предмета'


class BonusType(BaseNameValueDescriptionEnum):
    STRENGTH = auto(), 'Сила'
    CONSTITUTION = auto(), 'Телосложение'
    DEXTERITY = auto(), 'Ловкость'
    INTELLIGENCE = auto(), 'Интеллект'
    WISDOM = auto(), 'Мудрость'
    CHARISMA = auto(), 'Харизма'
    # --------------------------------
    ACROBATICS = auto(), 'Акробатика'
    ATHLETICS = auto(), 'Атлетика'
    PERCEPTION = auto(), 'Внимательность'
    THIEVERY = auto(), 'Воровство'
    ENDURANCE = auto(), 'Выносливость'
    INTIMIDATE = auto(), 'Запугивание'
    STREETWISE = auto(), 'Знание улиц'
    HISTORY = auto(), 'История'
    ARCANA = auto(), 'Магия'
    BLUFF = auto(), 'Обман'
    DIPLOMACY = auto(), 'Переговоры'
    DUNGEONEERING = auto(), 'Подземелья'
    NATURE = auto(), 'Природа'
    INSIGHT = auto(), 'Проницательность'
    RELIGION = auto(), 'Религия'
    STEALTH = auto(), 'Скрытность'
    HEAL = auto(), 'Целительство'
    # --------------------------------
    ARMOR_CLASS = auto(), 'КД'
    FORTITUDE = auto(), 'Стойкость'
    REFLEX = auto(), 'Реакция'
    WILL = auto(), 'Воля'
    # --------------------------------
    SPEED = auto(), 'Скорость'
    INITIATIVE = auto(), 'Инициатива'
    SURGE = auto(), 'Значение исцеления'
    SURGES = auto(), 'Количество исцелений'
    ATTACK = auto(), 'Атака'
