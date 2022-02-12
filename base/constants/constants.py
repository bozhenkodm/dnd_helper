from enum import Enum, auto
from random import randint

from base.constants.base import BaseNameValueDescriptionEnum, IntDescriptionEnum


class SexEnum(BaseNameValueDescriptionEnum):
    M = 'M', 'Муж'
    F = 'F', 'Жен'
    N = 'N', 'Н/Д'


class AbilitiesEnum(BaseNameValueDescriptionEnum):
    STRENGTH = 'STRENGTH', 'Сила'
    CONSTITUTION = 'CONSTITUTION', 'Телосложение'
    DEXTERITY = 'DEXTERITY', 'Ловкость'
    INTELLIGENCE = 'INTELLIGENCE', 'Интеллект'
    WISDOM = 'WISDOM', 'Мудрость'
    CHARISMA = 'CHARISMA', 'Харизма'


class PowersVariables(str, Enum):
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
    # (class bonus + half level + level bonus + enchantment). NOT +POWER ATTACK BONUS
    EHT = auto()  # armament enchantment
    ITL = auto()  # item level


class SizeEnum(BaseNameValueDescriptionEnum):
    TINY = 'TINY', 'Крошечный'
    SMALL = 'SMALL', 'Маленький'
    AVERAGE = 'AVERAGE', 'Средний'
    BIG = 'BIG', 'Большой'
    LARGE = 'LARGE', 'Огромный'


class VisionEnum(BaseNameValueDescriptionEnum):
    NORMAL = 'NORMAL', 'Обычное'
    TWILIGHT = 'TWILIGHT', 'Сумеречное'
    DARK = 'DARK', 'Тёмное'


class NPCRaceEnum(BaseNameValueDescriptionEnum):
    BUGBEAR = 'BUGBEAR', 'Багбир'
    VRYLOKA = 'VRYLOKA', 'Врылока'
    HAMADRYAD = 'HAMADRYAD', 'Гамадриада'
    GITHZERAI = 'GITHZERAI', 'Гитзерай'
    GNOME = 'GNOME', 'Гном'
    GNOLL = 'GNOLL', 'Гнолл'
    GOBLIN = 'GOBLIN', 'Гоблин'
    GOLIATH = 'GOLIATH', 'Голиаф'
    DWARF = 'DWARF', 'Дварф'
    DEVA = 'DEVA', 'Дев'
    GENASI_EARTHSOUL = 'GENASI_EARTHSOUL', 'Дженази, земля'
    GENASI_FIRESOUL = 'GENASI_FIRESOUL', 'Дженази, огонь'
    GENASI_STORMSOUL = 'GENASI_STORMSOUL', 'Дженази, шторм'
    GENASI_WATERSOUL = 'GENASI_WATERSOUL', 'Дженази, вода'
    GENASI_WINDSOUL = 'GENASI_WINDSOUL', 'Дженази, ветер'
    WILDEN = 'WILDEN', 'Дикарь'
    DOPPELGANGER = 'DOPPELGANGER', 'Доппельгангер'
    DRAGONBORN = 'DRAGONBORN', 'Драконорожденный'
    DROW = 'DROW', 'Дроу'
    DUERGAR = 'DUERGAR', 'Дуэргар'
    KALASHTAR = 'KALASHTAR', 'Калаштар'
    KENKU = 'KENKU', 'Кенку'
    KOBOLD = 'KOBOLD', 'Кобольд'
    WARFORGED = 'WARFORGED', 'Кованый'
    BLADELING = 'BLADELING', 'Мечерождённый'
    MINOTAUR = 'MINOTAUR', 'Минотавр'
    MUL = 'MUL', 'Мул'
    ORC = 'ORC', 'Орк'
    HALFELF = 'HALFELF', 'Полуэльф'
    HALFLING = 'HALFLING', 'Полурослик'
    HALFORC = 'HALFORC', 'Полуорк'
    PIXIE = 'PIXIE', 'Пикси'
    SATYR = 'SATYR', 'Сатир'
    TIEFLING = 'TIEFLING', 'Тифлинг'
    THRI_KREEN = 'THRI_KREEN', 'Три-крин'
    HOBGOBLIN = 'HOBGOBLIN', 'Хобгоблин'
    HUMAN = 'HUMAN', 'Человек'
    SHADAR_KAI = 'SHADAR_KAI', 'Шадар-Кай'
    SHIFTER_RAZORCLAW = 'SHIFTER_RAZORCLAW', 'Шифтер, бритволапый'
    SHIFTER_LONGTEETH = 'SHIFTER_LONGTEETH', 'Шифтер, длиннозубый'
    ELADRIN = 'ELADRIN', 'Эладрин'
    ELF = 'ELF', 'Эльф'


class NPCClassEnum(BaseNameValueDescriptionEnum):
    INVOKER = 'INVOKER', 'Апостол'
    ARTIFICER = 'ARTIFICER', 'Артефактор'
    BARD = 'BARD', 'Бард'
    VAMPIRE = 'VAMPIRE', 'Вампир'
    BARBARIAN = 'BARBARIAN', 'Варвар'
    WARLORD = 'WARLORD', 'Военачальник'
    WARPRIEST = 'WARPRIEST', 'Военный священник (жрец)'
    FIGHTER = 'FIGHTER', 'Воин'
    WIZARD = 'WIZARD', 'Волшебник'
    DRUID = 'DRUID', 'Друид'
    PRIEST = 'PRIEST', 'Жрец'
    SEEKER = 'SEEKER', 'Ловчий'
    AVENGER = 'AVENGER', 'Каратель'
    WARLOCK = 'WARLOCK', 'Колдун'
    SWORDMAGE = 'SWORDMAGE', 'Мечник-маг'
    MONK = 'MONK', 'Монах'
    PALADIN = 'PALADIN', 'Паладин'
    ROGUE = 'ROGUE', 'Плут'
    RUNEPRIEST = 'RUNEPRIEST', 'Рунный жрец'
    RANGER_MARKSMAN = 'RANGER_MARKSMAN', 'Следопыт (Дальнобойный)'
    RANGER_MELEE = 'RANGER_MELEE', 'Следопыт (Рукопашник)'
    HEXBLADE = 'HEXBLADE', 'Хексблэйд (колдун)'
    WARDEN = 'WARDEN', 'Хранитель'
    SORCERER = 'SORCERER', 'Чародей'
    SHAMAN = 'SHAMAN', 'Шаман'


class SkillsEnum(BaseNameValueDescriptionEnum):
    ACROBATICS = 'acrobatics', 'Акробатика'
    ARCANA = 'arcana', 'Магия'
    ATHLETICS = 'athletics', 'Атлетика'
    BLUFF = 'bluff', 'Обман'
    DIPLOMACY = 'diplomacy', 'Переговоры'
    DUNGEONEERING = 'dungeoneering', 'Подземелья'
    ENDURANCE = 'endurance', 'Выносливость'
    HEAL = 'heal', 'Целительство'
    HISTORY = 'history', 'История'
    INSIGHT = 'insight', 'Проницательность'
    INTIMIDATE = 'intimidate', 'Запугивание'
    NATURE = 'nature', 'Природа'
    PERCEPTION = 'perception', 'Внимательность'
    RELIGION = 'religion', 'Религия'
    STEALTH = 'stealth', 'Скрытность'
    STREETWISE = 'streetwise', 'Знание улиц'
    THIEVERY = 'thievery', 'Воровство'

    @classmethod
    def sequence(cls):
        yield from cls

    def get_base_ability(self):
        if self in (self.ACROBATICS, self.STEALTH, self.THIEVERY):
            return AbilitiesEnum.DEXTERITY
        if self in (self.ARCANA, self.HISTORY, self.RELIGION):
            return AbilitiesEnum.INTELLIGENCE
        if self == self.ATHLETICS:
            return AbilitiesEnum.STRENGTH
        if self in (self.BLUFF, self.DIPLOMACY, self.INTIMIDATE, self.STREETWISE):
            return AbilitiesEnum.CHARISMA
        if self in (
            self.DUNGEONEERING,
            self.HEAL,
            self.INSIGHT,
            self.NATURE,
            self.PERCEPTION,
        ):
            return AbilitiesEnum.WISDOM
        if self == self.ENDURANCE:
            return AbilitiesEnum.CONSTITUTION


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
    def penalty(self):
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
    # Melee
    AXE = 'AXE', 'Топор'
    MACE = 'MACE', 'Булава'
    LIGHT_BLADE = 'LIGHT_BLADE', 'Лёгкий клинок'
    SPEAR = 'SPEAR', 'Копьё'
    STAFF = 'STAFF', 'Посох'
    FLAIL = 'FLAIL', 'Цеп'
    HEAVY_BLADE = 'HEAVY_BLADE', 'Тяжелый клинок'
    HAMMER = 'HAMMER', 'Молот'
    PICK = 'PICK', 'Кирка'
    POLEARM = 'POLEARM', 'Древковое'
    UNARMED = 'UNARMED', 'Безоружное'
    # Ranged
    SLING = 'SLING', 'Праща'
    CROSSBOW = 'CROSSBOW', 'Арбалет'
    BOW = 'BOW', 'Лук'


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
    ONE = 'one', 'Одноручное'
    TWO = 'two', 'Двуручное'
    VERSATILE = (
        'versatile',
        'Универсальное',
    )  # one handed, but can be used with two hands
    # (with +1 to damage, unless user is small)


class PowerSourceEnum(BaseNameValueDescriptionEnum):
    MARTIAL = 'martial', 'Воинский'
    DIVINE = 'divine', 'Духовный'
    ARCANE = 'arcane', 'Магический'
    PRIMAL = 'primal', 'Первородный'
    SHADOW = 'shadow', 'Теневой'
    PSIONIC = 'psionic', 'Псионический'


class ClassRoleEnum(BaseNameValueDescriptionEnum):
    STRIKER = 'striker', 'Атакующий'
    DEFENDER = 'defender', 'Защитник'
    CONTROLLER = 'controller', 'Контроллер'
    LEADER = 'leader', 'Лидер'


class PowerFrequencyEnum(BaseNameValueDescriptionEnum):
    PASSIVE = 'PASSIVE', 'Пассивный'
    AT_WILL = 'AT_WILL', 'Неограниченный'
    ENCOUNTER = 'ENCOUNTER', 'На сцену'
    DAYLY = 'DAYLY', 'На день'


class PowerDamageTypeEnum(BaseNameValueDescriptionEnum):
    NONE = 'NONE', ''
    ACID = 'ACID', 'Кислота'
    COLD = 'COLD', 'Холод'
    FIRE = 'FIRE', 'Огонь'
    LIGHTNING = 'LIGHTNING', 'Электричество'
    NECROTIC = 'NECROTIC', 'Некротическая энергия'
    POISON = 'POISON', 'Яд'
    PSYCHIC = 'PSYCHIC', 'Психическая энергия'
    RADIANT = 'RADIANT', 'Излучение'
    THUNDER = 'THUNDER', 'Звук'
    FORCE = 'FORCE', 'Силовое поле'


class PowerEffectTypeEnum(BaseNameValueDescriptionEnum):
    NONE = 'NONE', ''
    CHARM = 'CHARM', 'Очарование'
    CONJURATION = 'CONJURATION', 'Иллюзия'
    FEAR = 'FEAR', 'Страх'
    HEALING = 'HEALING', 'Исцеление'
    INVIGORATING = 'INVIGORATING', 'Укрепляющий'
    POLYMORPH = 'POLYMORPH', 'Превращение'
    RAGE = 'RAGE', 'Ярость'
    RATTLING = 'RATTLING', 'Ужасающий'
    RELIABLE = 'RELIABLE', 'Надежный'
    SLEEP = 'SLEEP', 'Сон'
    STANCE = 'STANCE', 'Стойка'
    TELEPORTATION = 'TELEPORTATION', 'Телепортация'
    ZONE = 'ZONE', 'Зона'


class PowerActionTypeEnum(BaseNameValueDescriptionEnum):
    STANDARD = 'STANDARD', 'Стандартное действие'
    MINOR = 'MINOR', 'Малое действие'
    FREE = 'FREE', 'Свободное действие'
    MOVEMENT = 'MOVEMENT', 'Действие движения'
    PROVOKED = 'PROVOKED', 'Провоцированное действие'
    INTERRUPT = 'INTERRUPT', 'Немедленное прерывание'
    REACTION = 'REACTION', 'Немедленный ответ'
    NO_ACTION = 'NO_ACTION', 'Нет действия'


class AccessoryTypeEnum(BaseNameValueDescriptionEnum):
    IMPLEMENT = 'IMPLEMENT', 'Инструмент'
    WEAPON = 'WEAPON', 'Оружие'
    TWO_WEAPONS = 'TWO_WEAPONS', 'Два оружия'
    # WEAPON_AND_IMPLEMENT = 'WEAPON_AND_IMPLEMENT', 'Оружие и инструмент'


class DefenceTypeEnum(BaseNameValueDescriptionEnum):
    ARMOR_CLASS = 'ARMOR_CLASS', 'КД'
    FORTITUDE = 'FORTITUDE', 'Стойкость'
    REFLEX = 'REFLEX', 'Реакция'
    WILL = 'WILL', 'Воля'


class PowerRangeTypeEnum(BaseNameValueDescriptionEnum):
    MELEE_WEAPON = 'MELEE_WEAPON', 'Рукопашное оружие'
    MELEE = 'MELEE', 'Рукопашное'
    RANGED = 'RANGED', 'Дальнобойное'
    MELEE_RANGED_WEAPON = 'MELEE_RANGED_WEAPON', 'Рукопашное или дальнобойное оружие'
    RANGED_WEAPON = 'RANGED_WEAPON', 'Дальнобойное оружие'
    BURST = 'BURST', 'Вспышка'
    BLAST = 'BLAST', 'Волна'
    WALL = 'WALL', 'Стена'
    PERSONAL = 'PERSONAL', 'Персональный'

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


class PowerPropertyTitle(BaseNameValueDescriptionEnum):
    ATTACK = 'ATTACK', 'Атака'
    HIT = 'HIT', 'Попадание'
    MISS = 'MISS', 'Промах'
    EFFECT = 'EFFECT', 'Эффект'
    REQUIREMENT = 'REQUIREMENT', 'Требование'
    TRIGGER = 'TRIGGER', 'Триггер'
    SPECIAL = 'SPECIAL', 'Особенность'
    TARGET = 'TARGET', 'Цель'
    OTHER = 'OTHER', 'Другое'


class MagicItemCategory(BaseNameValueDescriptionEnum):
    COMMON = 'COMMON', 'Обычный'
    UNCOMMON = 'UNCOMMON', 'Необычный'
    RARE = 'RARE', 'Редкий'


class MagicItemSlot(BaseNameValueDescriptionEnum):
    WEAPON = 'weapon', 'Оружие'
    ARMOR = 'armor', 'Броня'
    NECK = 'neck', 'Шея'
    HEAD = 'head', 'Голова'
    ARMS = 'arms', 'Предплечья/Щит'
    FEET = 'feet', 'Обувь'
    HANDS = 'hands', 'Перчатки'
    WAIST = 'waist', 'Пояс'
    RING = 'ring', 'Кольца'
    WONDROUS_ITEMS = 'wondrous_items', 'Чудесный предмет'
    TATOO = 'tatoo', 'Татуировка'
