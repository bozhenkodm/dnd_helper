from enum import StrEnum, auto
from random import randint

from base.constants.base import BaseNameValueDescriptionEnum, IntDescriptionEnum


class SexEnum(BaseNameValueDescriptionEnum):
    M = auto(), 'Муж'
    F = auto(), 'Жен'
    N = auto(), 'Н/Д'


class AbilityEnum(BaseNameValueDescriptionEnum):
    STRENGTH = auto(), 'Сила'
    CONSTITUTION = auto(), 'Телосложение'
    DEXTERITY = auto(), 'Ловкость'
    INTELLIGENCE = auto(), 'Интеллект'
    WISDOM = auto(), 'Мудрость'
    CHARISMA = auto(), 'Харизма'


# noinspection PyArgumentList
class PowerVariables(StrEnum):
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
    DMS = auto()  # secondary weapon damage bonus
    ATK = auto()  # attack bonus =
    # (class bonus + half level + level bonus + enhancement). NOT +POWER ATTACK BONUS
    ATS = auto()  # secondary weapon attack bonus
    EHT = auto()  # armament enhancement
    EHS = auto()  # secondary weapon armament enhancement
    ITL = auto()  # item level


class SizeIntEnum(IntDescriptionEnum):
    TINY = -1, 'Крошечный'
    SMALL = 0, 'Маленький'
    AVERAGE = 1, 'Средний'
    BIG = 2, 'Большой'
    LARGE = 3, 'Огромный'


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
    HEXBLADE = auto(), 'Хексблэйд (колдун)'
    WARDEN = auto(), 'Хранитель'
    SORCERER = auto(), 'Чародей'
    SHAMAN = auto(), 'Шаман'


class SkillEnum(BaseNameValueDescriptionEnum):
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
            return -2
        return 0


class WeaponGroupEnum(BaseNameValueDescriptionEnum):
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
    OFF_HAND = auto(), 'Дополнительное'
    ONE = auto(), 'Одноручное'
    VERSATILE = (
        auto(),
        'Универсальное',
    )  # one-handed, but can be used with two hands
    # (with +1 to damage, unless user is small)
    TWO = auto(), 'Двуручное'
    FREE = auto(), 'Не занимает руки'  # ki and symbols of faith


class PowerSourceEnum(BaseNameValueDescriptionEnum):
    MARTIAL = auto(), 'Воинский'
    DIVINE = auto(), 'Духовный'
    ARCANE = auto(), 'Магический'
    PRIMAL = auto(), 'Первородный'
    SHADOW = auto(), 'Теневой'
    PSIONIC = auto(), 'Псионический'


class PowerSourceIntEnum(IntDescriptionEnum):
    # workaround to not make another
    # PropertiesCondition model for strings
    # maybe change power source and role to int
    MARTIAL = 1, 'Воинский'
    DIVINE = 2, 'Духовный'
    ARCANE = 3, 'Магический'
    PRIMAL = 4, 'Первородный'
    SHADOW = 5, 'Теневой'
    PSIONIC = 6, 'Псионический'


class ClassRoleEnum(BaseNameValueDescriptionEnum):
    STRIKER = auto(), 'Атакующий'
    DEFENDER = auto(), 'Защитник'
    CONTROLLER = auto(), 'Контроллер'
    LEADER = auto(), 'Лидер'


class ClassRoleIntEnum(IntDescriptionEnum):
    # see comment to PowerSourceIntEnum
    STRIKER = 1, 'Атакующий'
    DEFENDER = 2, 'Защитник'
    CONTROLLER = 3, 'Контроллер'
    LEADER = 4, 'Лидер'


class PowerFrequencyIntEnum(IntDescriptionEnum):
    PASSIVE = 0, 'Пассивный'
    AT_WILL = 1, 'Неограниченный'
    ENCOUNTER = 2, 'На сцену'
    DAILY = 3, 'На день'


class PowerDamageTypeEnum(BaseNameValueDescriptionEnum):
    UNTYPED = auto(), 'Без типа'
    THUNDER = auto(), 'Звук'
    RADIANT = auto(), 'Излучение'
    ACID = auto(), 'Кислота'
    NECROTIC = auto(), 'Некротическая энергия'
    FIRE = auto(), 'Огонь'
    PSYCHIC = auto(), 'Психическая энергия'
    FORCE = auto(), 'Силовое поле'
    COLD = auto(), 'Холод'
    LIGHTNING = auto(), 'Электричество'
    POISON = auto(), 'Яд'


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
    WEAPON_AND_IMPLEMENT = auto(), 'Оружие и инструмент'


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
        )


class ThrownWeaponType(BaseNameValueDescriptionEnum):
    LIGHT = auto(), 'Лёгкое метательное'
    HEAVY = auto(), 'Тяжёлое метательное'


class BonusSource(BaseNameValueDescriptionEnum):
    CLASS = auto(), 'Бонус класса'
    RACE = auto(), 'Расовый бонус'
    POWER = auto(), 'Бонус таланта'
    FEAT = auto(), 'Бонус черты'
    ITEM = auto(), 'Бонус предмета'
    SHIELD = auto(), 'Бонус щита'


class NPCOtherProperties(BaseNameValueDescriptionEnum):
    SPEED = auto(), 'Скорость'
    INITIATIVE = auto(), 'Инициатива'
    SURGE = auto(), 'Значение исцеления'
    SURGES = auto(), 'Количество исцелений'
    HIT_POINTS = auto(), 'Количество хитов'
    POWER_SOURCE = auto(), 'Источник силы'
    ROLE = auto(), 'Роль'
    SIZE = auto(), 'Размер'
    SPEED_PENALTY = auto(), 'Штраф скорости'
    SKILL_PENALTY = auto(), 'Штраф навыков'
    ATTACK = auto(), 'Атака'
    DAMAGE = auto(), 'Урон'


MODEL_NAME_TO_NPC_FIELD = {
    'class': 'klass',
    'functionaltemplate': 'functional_template',
    'paragonpath': 'paragon_path',
    'power': 'powers',
    'feat': 'feats',
    'skill': 'trained_skills',
}
