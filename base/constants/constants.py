from enum import Enum, auto
from random import randint

from base.constants.base import BaseNameValueDescriptionEnum, IntDescriptionEnum


class SexEnum(BaseNameValueDescriptionEnum):
    M = 'M', 'Муж'
    F = 'F', 'Жен'
    N = 'N', 'Н/Д'


class AbilitiesEnum(BaseNameValueDescriptionEnum):
    STRENGTH = 'strength', 'Сила'
    CONSTITUTION = 'constitution', 'Телосложение'
    DEXTERITY = 'dexterity', 'Ловкость'
    INTELLIGENCE = 'intelligence', 'Интеллект'
    WISDOM = 'wisdom', 'Мудрость'
    CHARISMA = 'charisma', 'Харизма'


# noinspection PyArgumentList
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
    INVOKER = 'invoker', 'Апостол'
    ARTIFICER = 'artificer', 'Артефактор'
    BARD = 'bard', 'Бард'
    BLADESINGER = 'bladesinger', 'Блэйдсингер'
    VAMPIRE = 'vampire', 'Вампир'
    BARBARIAN = 'barbarian', 'Варвар'
    WARLORD = 'warlord', 'Военачальник'
    WARPRIEST = 'warpriest', 'Военный священник (жрец)'
    FIGHTER = 'fighter', 'Воин'
    WIZARD = 'wizard', 'Волшебник'
    DRUID = 'druid', 'Друид'
    PRIEST = 'priest', 'Жрец'
    SEEKER = 'seeker', 'Ловчий'
    AVENGER = 'avenger', 'Каратель'
    WARLOCK = 'warlock', 'Колдун'
    SWORDMAGE = 'swordmage', 'Мечник-маг'
    MONK = 'monk', 'Монах'
    PALADIN = 'paladin', 'Паладин'
    ROGUE = 'rogue', 'Плут'
    RUNEPRIEST = 'runepriest', 'Рунный жрец'
    RANGER = 'ranger', 'Следопыт'
    RANGER_MELEE = 'ranger_melee', 'Следопыт (Рукопашник)'
    HEXBLADE = 'hexblade', 'Хексблэйд (колдун)'
    WARDEN = 'warden', 'Хранитель'
    SORCERER = 'sorcerer', 'Чародей'
    SHAMAN = 'shaman', 'Шаман'


class SkillsEnum(BaseNameValueDescriptionEnum):
    ACROBATICS = 'acrobatics', 'Акробатика'
    ATHLETICS = 'athletics', 'Атлетика'
    PERCEPTION = 'perception', 'Внимательность'
    THIEVERY = 'thievery', 'Воровство'
    ENDURANCE = 'endurance', 'Выносливость'
    INTIMIDATE = 'intimidate', 'Запугивание'
    STREETWISE = 'streetwise', 'Знание улиц'
    HISTORY = 'history', 'История'
    ARCANA = 'arcana', 'Магия'
    BLUFF = 'bluff', 'Обман'
    DIPLOMACY = 'diplomacy', 'Переговоры'
    DUNGEONEERING = 'dungeoneering', 'Подземелья'
    NATURE = 'nature', 'Природа'
    INSIGHT = 'insight', 'Проницательность'
    RELIGION = 'religion', 'Религия'
    STEALTH = 'stealth', 'Скрытность'
    HEAL = 'heal', 'Целительство'

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
    # Melee
    AXE = 'axe', 'Топор'
    MACE = 'mace', 'Булава'
    LIGHT_BLADE = 'light_blade', 'Лёгкий клинок'
    SPEAR = 'spear', 'Копьё'
    STAFF = 'staff', 'Посох'
    FLAIL = 'flail', 'Цеп'
    HEAVY_BLADE = 'heavy_blade', 'Тяжелый клинок'
    HAMMER = 'hammer', 'Молот'
    PICK = 'pick', 'Кирка'
    POLEARM = 'polearm', 'Древковое'
    UNARMED = 'unarmed', 'Безоружное'
    # Ranged
    SLING = 'sling', 'Праща'
    CROSSBOW = 'crossbow', 'Арбалет'
    BOW = 'bow', 'Лук'


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
    )  # one-handed, but can be used with two hands
    # (with +1 to damage, unless user is small)
    FREE = 'free', 'Не занимает руки'  # ki and symbols of faith


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
    DAILY = 'DAILY', 'На день'


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

    @property
    def is_melee_weapon(self):
        return self in (self.MELEE_WEAPON, self.MELEE_RANGED_WEAPON)

    @property
    def is_ranged_weapon(self):
        return self in (self.RANGED_WEAPON, self.MELEE_RANGED_WEAPON)


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


class NPCCreationStepEnum(IntDescriptionEnum):
    BASE = 1, 'Базовая информация'
    BASE_ABILITIES = 2, 'Базовые характеристики'
    LEVEL_BONUS_ABILITIES = 3, 'Бонусы характеристик от уровня'
    SKILLS = 4, 'Навыки'
    ITEMS = 5, 'Предметы'
    WEAPONS = 6, 'Вооружение'
