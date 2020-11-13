from django.core import validators
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

from base.constants import (
    ArmorTypeEnum,
    AttributesEnum,
    DamageDice,
    NPCClass,
    NPCRace,
    SexEnum,
    ShieldTypeEnum,
    SizeEnum,
    SkillsEnum,
    VisionEnum,
    WeaponCategory,
    WeaponGroup,
)
from base.models.mixins.attributes import AttributeMixin
from base.models.mixins.skills import SkillMixin


class Armor(models.Model):
    class Meta:
        verbose_name = 'Доспех'
        verbose_name_plural = 'Доспехи'

    name = models.CharField(verbose_name='Название', max_length=20)
    armor_type = models.CharField(
        verbose_name='Тип',
        choices=ArmorTypeEnum.generate_choices(is_sorted=False),
        max_length=ArmorTypeEnum.max_length(),
    )
    armor_class = models.SmallIntegerField(verbose_name='Класс доспеха', default=0)
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)
    speed_penalty = models.SmallIntegerField(verbose_name='Штраф скорости', default=0)
    skill_penalty = models.SmallIntegerField(verbose_name='Штраф навыков', default=0)

    def __str__(self):
        return (
            f'{self.name}, {ArmorTypeEnum[self.armor_type].value}, +{self.enchantment}'
        )

    @property
    def is_light(self):
        return self.armor_type in (
            ArmorTypeEnum.CLOTH.name,
            ArmorTypeEnum.LEATHER.name,
            ArmorTypeEnum.HIDE.name,
        )


class WeaponType(models.Model):
    class Meta:
        verbose_name = 'Тип оружия'
        verbose_name_plural = 'Типы оружия'

    name = models.CharField(verbose_name='Название', max_length=20)
    prof_bonus = models.SmallIntegerField(verbose_name='Бонус владения', default=2)
    group = models.CharField(
        verbose_name='Группа оружия',
        choices=WeaponGroup.generate_choices(),
        max_length=WeaponGroup.max_length(),
    )
    category = models.CharField(
        verbose_name='Категория',
        choices=WeaponCategory.generate_choices(),
        max_length=WeaponCategory.max_length(),
    )
    damage = models.CharField(
        verbose_name='Кость урона', choices=DamageDice.generate_choices(), max_length=5
    )

    def __str__(self):
        return self.name


class Weapon(models.Model):
    class Meta:
        verbose_name = 'Оружие'
        verbose_name_plural = 'Оружие'

    weapon_type = models.ForeignKey(WeaponType, on_delete=models.CASCADE, null=False)
    name = models.CharField(verbose_name='Название', max_length=20)
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)

    @property
    def full_name(self):
        return f'{self.weapon_type.name}, {self.name}'

    def __str__(self):
        return self.full_name


class ImplementType(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20)


class Implement(models.Model):
    implement_type = models.ForeignKey(
        ImplementType, on_delete=models.CASCADE, null=True
    )
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)


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


class RaceBonus(models.Model):
    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'

    name = models.CharField(verbose_name='Название', max_length=30, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    def __str__(self):
        return f'Бонус расы: {self.race.get_name_display()}'


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
    available_weapon_category = MultiSelectField(
        verbose_name='Владение категориями оружия',
        choices=WeaponCategory.generate_choices(is_sorted=False),
        null=True,
    )
    available_weapon_type = models.ManyToManyField(
        WeaponType, verbose_name='Владение оружием', blank=True
    )
    is_weapon_implement = models.BooleanField(
        verbose_name='Оружие как инструмент', default=False
    )
    available_implement_type = models.ManyToManyField(
        ImplementType, verbose_name='Доступные инструменты', blank=True
    )
    hit_points_per_level = models.PositiveSmallIntegerField(
        verbose_name='Хитов за уровень', default=8
    )

    def __str__(self):
        return NPCClass[self.name].value


class NPC(AttributeMixin, SkillMixin, models.Model):
    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCS'

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
        max_length=SexEnum.max_length(),
        choices=SexEnum.generate_choices(is_sorted=False),
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

    weapons = models.ManyToManyField(Weapon, verbose_name='Оружие')
    implements = models.ManyToManyField(Implement, verbose_name='Инструменты')
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
        result = self.bloodied // 2
        # У драконорождённых исцеление увеличено
        if self.race.name == NPCRace.DRAGONBORN.name:
            result += self.modifier(self.constitution)
        return result

    @property
    def _tier(self):
        """Этап развития"""
        if self.level < 11:
            return 0
        if self.level >= 21:
            return 2
        return 1

    @property
    def surges(self):
        """Количество исцелений"""
        return self._tier + 1

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
        if self.klass.name == NPCClass.BARBARIAN.name:
            if not self.shield and self.armor.is_light:
                result += (self.level - 1) // 10 + 1
        if self.klass.name == NPCClass.AVENGER.name:
            if not self.shield and (
                not self.armor or self.armor.type == ArmorTypeEnum.CLOTH.name
            ):
                result += 3
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
        if self.klass.name == NPCClass.BARBARIAN.name:
            if not self.shield and self.armor.is_light:
                result += (self.level - 1) // 10 + 1
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

    @property
    def url(self):
        return reverse('encounter', kwargs={'pk': self.pk})
