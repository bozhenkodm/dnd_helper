from collections import Counter

from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

from base.constants import (
    ArmorTypeEnum,
    AttributesEnum,
    NPCClass,
    NPCRace,
    ShieldTypeEnum,
    SizeEnum,
    SkillsEnum,
    VisionEnum,
)


class Race(models.Model):
    class Meta:
        verbose_name = 'Раса'
        verbose_name_plural = 'Расы'

    name = models.CharField(
        verbose_name='Название',
        max_length=NPCRace.max_length(),
        choices=NPCRace.generate_choices(),
        unique=True,
    )
    speed = models.PositiveSmallIntegerField(default=6, verbose_name='Скорость')
    const_bonus_attrs = MultiSelectField(
        verbose_name='Обязательные бонусы характеристик',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    var_bonus_attrs = MultiSelectField(
        verbose_name='Выборочные бонусы характеристик',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )
    size = models.CharField(
        verbose_name='Размер',
        max_length=SizeEnum.max_length(),
        choices=SizeEnum.generate_choices(is_sorted=False),
        default=SizeEnum.AVERAGE.name,
    )
    vision = models.CharField(
        verbose_name='Зрение',
        max_length=VisionEnum.max_length(),
        choices=VisionEnum.generate_choices(),
        default=VisionEnum.TWILIGHT.name,
    )

    fortitude_bonus = models.SmallIntegerField(
        verbose_name='Бонус стойкости', default=0
    )
    reflex_bonus = models.SmallIntegerField(verbose_name='Бонус реакции', default=0)
    will_bonus = models.SmallIntegerField(verbose_name='Бонус воли', default=0)

    skill_bonuses = MultiSelectField(
        verbose_name='Бонусы навыков',
        choices=SkillsEnum.generate_choices(),
        max_choices=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return NPCRace[self.name].value

    @property
    def test(self):
        return self.get_name_display()


class RaceBonus(models.Model):
    bonus = models.TextField()
    race = models.ForeignKey(Race, on_delete=models.CASCADE)


class Class(models.Model):
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    name = models.CharField(
        verbose_name='Название',
        max_length=NPCClass.max_length(),
        choices=NPCClass.generate_choices(),
        unique=True,
    )
    fortitude_bonus = models.SmallIntegerField(
        verbose_name='Бонус стойкости', default=0
    )
    reflex_bonus = models.SmallIntegerField(verbose_name='Бонус реакции', default=0)
    will_bonus = models.SmallIntegerField(verbose_name='Бонус воли', default=0)
    trained_skills = MultiSelectField(
        verbose_name='Тренированные навыки',
        choices=SkillsEnum.generate_choices(),
        min_choices=1,
        null=True,
        blank=True,
    )
    available_armor_types = MultiSelectField(
        verbose_name='Ношение доспехов',
        choices=ArmorTypeEnum.generate_choices(is_sorted=False),
        default=ArmorTypeEnum.CLOTH.name,
    )
    available_shield_types = MultiSelectField(
        verbose_name='Ношение щитов',
        choices=ShieldTypeEnum.generate_choices(),
        blank=True,
        null=True,
    )
    hit_points_per_level = models.PositiveSmallIntegerField(
        verbose_name='Хитов за уровень', default=8
    )

    def __str__(self):
        return NPCClass[self.name].value


class Armor(models.Model):
    class Meta:
        verbose_name = 'Доспех'
        verbose_name_plural = 'Доспехи'

    name = models.CharField(verbose_name='Название', max_length=20)
    type = models.CharField(
        verbose_name='Тип',
        choices=ArmorTypeEnum.generate_choices(is_sorted=False),
        max_length=ArmorTypeEnum.max_length(),
    )
    armor_class = models.SmallIntegerField(verbose_name='Класс доспеха', default=0)
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)
    speed_penalty = models.SmallIntegerField(verbose_name='Штраф скорости', default=0)
    skill_penalty = models.SmallIntegerField(verbose_name='Штраф навыков', default=0)

    def __str__(self):
        return f'{self.name}, {ArmorTypeEnum[self.type].value} +{self.enchantment}'

    @property
    def is_light(self):
        return self.type in (
            ArmorTypeEnum.CLOTH.name,
            ArmorTypeEnum.LEATHER.name,
            ArmorTypeEnum.HIDE.name,
        )


class NPC(models.Model):
    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCS'

    SEX_CHOICES = (('M', 'М'), ('F', 'Ж'), ('N', '-'))

    name = models.CharField(verbose_name='Имя', max_length=50)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        verbose_name='Раса',
    )
    klass = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name='Класс',
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='Пол',
    )

    level = models.PositiveSmallIntegerField(
        verbose_name='Уровень',
    )

    base_strength = models.PositiveSmallIntegerField(verbose_name='Сила (базовая)')
    base_constitution = models.PositiveSmallIntegerField(
        verbose_name='Телосложение (базовое)',
    )
    base_dexterity = models.PositiveSmallIntegerField(
        verbose_name='Ловкость (базовая)',
    )
    base_intelligence = models.PositiveSmallIntegerField(
        verbose_name='Интеллект (базовый)',
    )
    base_wisdom = models.PositiveSmallIntegerField(
        verbose_name='Мудрость (базовая)',
    )
    base_charisma = models.PositiveSmallIntegerField(
        verbose_name='Харизма (базовая)',
    )

    var_bonus_attr = models.CharField(
        verbose_name='Выборочный бонус характеристики',
        max_length=AttributesEnum.max_length(),
        choices=AttributesEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )

    level4_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 4 уровне',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level8_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 8 уровне',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level14_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 14 уровне',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level18_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 18 уровне',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level24_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 24 уровне',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level28_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 28 уровне',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )

    trained_skills = MultiSelectField(
        verbose_name='Тренированные навыки',
        choices=SkillsEnum.generate_choices(),
        min_choices=1,
        null=True,
        blank=True,
    )

    armor = models.ForeignKey(
        Armor, verbose_name='Доспехи', null=True, on_delete=models.SET_NULL
    )

    shield = models.CharField(
        verbose_name='Щит',
        max_length=5,
        choices=ShieldTypeEnum.generate_choices(),
        null=True,
        blank=True,
    )
    attack_attributes = MultiSelectField(
        verbose_name='Атакующие характеристики',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        default=AttributesEnum.STRENGTH.name,
    )
    attack_bonus = models.SmallIntegerField(
        verbose_name='Бонус атаки (Оружие, инструменты + заточка', default=0
    )

    def __str__(self):
        return f'{self.name} {self.race} {self.klass} {self.level} уровня'

    @property
    def url(self):
        return reverse('npc', kwargs={'pk': self.pk})

    @property
    def half_level(self):
        return self.level // 2

    @property
    def _magic_threshold(self):
        """ Магический порог (максимальный бонус от магических предметов)"""
        return self.level // 5 + 1

    @property
    def _level_bonus(self):
        """ Условный бонус к защитам, атакам и урону для мастерских персонажей"""
        return ((self.level - 1) // 5) * 2 + 1

    @property
    def max_hit_points(self):
        return self.klass.hit_points_per_level * self.level + self.constitution

    @property
    def bloodied(self):
        return self.max_hit_points // 2

    @property
    def surge(self):
        """
        Исцеление
        """
        return self.bloodied // 2

    @property
    def surges(self):
        """Количество исцелений"""
        if self.level <= 10:
            return 1
        if self.level >= 21:
            return 3
        return 2

    @staticmethod
    def modifier(value):
        return (value - 10) // 2

    @property
    def armor_class(self):
        result = 10 + self.half_level + self._level_bonus
        if self.armor:
            if self.armor.type in self.klass.available_armor_types:
                result += self.armor.armor_class
            result += self.armor.enchantment
        if not self.armor or self.armor.is_light:
            result += max(
                self.modifier(self.dexterity), self.modifier(self.intelligence)
            )
        if self.shield and self.shield in self.klass.available_shield_types:
            if self.shield == ShieldTypeEnum.LIGHT.name:
                result += 1
            else:
                result += 2
        return result

    @property
    def attacks(self):
        """Общий бонус атаки"""
        return (
            (
                AttributesEnum[name].value,
                self.half_level
                + self._level_bonus
                + self.attack_bonus
                + self.modifier(getattr(self, name.lower())),
            )
            for name in self.attack_attributes
        )

    @property
    def fortitude(self):
        return (
            10
            + self.half_level
            + self._level_bonus
            + max(self.modifier(self.strength), self.modifier(self.constitution))
        )

    @property
    def reflex(self):
        result = (
            10
            + self.half_level
            + self._level_bonus
            + max(self.modifier(self.dexterity), self.modifier(self.intelligence))
        )
        if self.shield and self.shield in self.klass.available_shield_types:
            if self.shield == ShieldTypeEnum.LIGHT.name:
                result += 1
            else:
                result += 2
        return result

    @property
    def will(self):
        return (
            10
            + self.half_level
            + self._level_bonus
            + max(self.modifier(self.wisdom), self.modifier(self.charisma))
        )

    @property
    def initiative(self):
        return self.modifier(self.dexterity) + self.half_level

    @property
    def _initial_attr_bonuses(self):
        bonus_attrs = self.race.const_bonus_attrs
        bonus_attrs.append(self.var_bonus_attr)
        bonus_attrs = {key: 2 for key in bonus_attrs}
        return bonus_attrs

    @property
    def _level_attr_bonuses(self):
        bonus_attrs = (
            (self.level4_bonus_attrs or [])
            + (self.level8_bonus_attrs or [])
            + (self.level14_bonus_attrs or [])
            + (self.level18_bonus_attrs or [])
            + (self.level24_bonus_attrs or [])
            + (self.level28_bonus_attrs or [])
        )
        return Counter(bonus_attrs)

    @property
    def _tier_attrs_bonus(self):
        if self.level > 21:
            return 2
        if self.level > 11:
            return 1
        return 0

    def _calculate_attribute_bonus(self, attribute: AttributesEnum):
        return (
            self._initial_attr_bonuses.get(attribute.name, 0)
            + self._tier_attrs_bonus
            + self._level_attr_bonuses[attribute.name]
        )

    @property
    def strength(self):
        return self.base_strength + self._calculate_attribute_bonus(
            AttributesEnum.STRENGTH
        )

    @property
    def constitution(self):
        return self.base_constitution + self._calculate_attribute_bonus(
            AttributesEnum.CONSTITUTION
        )

    @property
    def dexterity(self):
        return self.base_dexterity + self._calculate_attribute_bonus(
            AttributesEnum.DEXTERITY
        )

    @property
    def intelligence(self):
        return self.base_intelligence + self._calculate_attribute_bonus(
            AttributesEnum.INTELLIGENCE
        )

    @property
    def wisdom(self):
        return self.base_wisdom + self._calculate_attribute_bonus(AttributesEnum.WISDOM)

    @property
    def charisma(self):
        return self.base_charisma + self._calculate_attribute_bonus(
            AttributesEnum.CHARISMA
        )

    @property
    def _trained_skills_bonuses(self):
        return {key: 5 for key in self.trained_skills}

    def _calculate_skill(self, skill: SkillsEnum) -> int:
        attribute = getattr(self, skill.get_base_attribute().name.lower())
        result = (
            self.half_level
            + self.modifier(attribute)
            + self._trained_skills_bonuses.get(skill.name, 0)
        )
        if skill in (
            SkillsEnum.ACROBATICS,
            SkillsEnum.ATHLETICS,
            SkillsEnum.THIEVERY,
            SkillsEnum.ENDURANCE,
            SkillsEnum.STEALTH,
        ):
            result -= self.armor.skill_penalty
        return result

    @property
    def acrobatics(self):
        """Акробатика"""
        return self._calculate_skill(SkillsEnum.ACROBATICS)

    @property
    def arcana(self):
        """Магия"""
        return self._calculate_skill(SkillsEnum.ARCANA)

    @property
    def athletics(self):
        """Атлетика"""
        return self._calculate_skill(SkillsEnum.ATHLETICS)

    @property
    def bluff(self):
        """Обман"""
        return self._calculate_skill(SkillsEnum.BLUFF)

    @property
    def diplomacy(self):
        """Переговоры"""
        return self._calculate_skill(SkillsEnum.DIPLOMACY)

    @property
    def dungeoneering(self):
        """Подземелья"""
        return self._calculate_skill(SkillsEnum.DUNGEONEERING)

    @property
    def endurance(self):
        """Выносливость"""
        return self._calculate_skill(SkillsEnum.ENDURANCE)

    @property
    def heal(self):
        """Целительство"""
        return self._calculate_skill(SkillsEnum.HEAL)

    @property
    def history(self):
        """История"""
        return self._calculate_skill(SkillsEnum.HISTORY)

    @property
    def insight(self):
        """Внимательность"""
        return self._calculate_skill(SkillsEnum.INSIGHT)

    @property
    def intimidate(self):
        """Запугивание"""
        return self._calculate_skill(SkillsEnum.INTIMIDATE)

    @property
    def nature(self):
        """Природа"""
        return self._calculate_skill(SkillsEnum.NATURE)

    @property
    def perception(self):
        """Проницательность"""
        return self._calculate_skill(SkillsEnum.PERCEPTION)

    @property
    def religion(self):
        """Религия"""
        return self._calculate_skill(SkillsEnum.RELIGION)

    @property
    def stealth(self):
        """Скрытность"""
        return self._calculate_skill(SkillsEnum.STEALTH)

    @property
    def streetwise(self):
        """Знание_улиц"""
        return self._calculate_skill(SkillsEnum.STREETWISE)

    @property
    def thievery(self):
        """Воровство"""
        return self._calculate_skill(SkillsEnum.THIEVERY)


class Encounter(models.Model):
    class Meta:
        verbose_name = 'Сцена'
        verbose_name_plural = 'Сцены'

    short_description = models.CharField(
        max_length=30, verbose_name='Краткое описание', null=True, blank=True
    )
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    npcs = models.ManyToManyField(NPC, verbose_name='Мастерские персонажи')

    def __str__(self):
        if self.short_description:
            return f'Сцена {self.short_description}'
        return f'Сцена №{self.id}'
