from django.core import validators
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

from base.constants import (
    AccessoryTypeEnum,
    ArmorTypeEnum,
    AttributesEnum,
    DefenceTypeEnum,
    DiceEnum,
    NPCClassEnum,
    NPCRaceEnum,
    PowerActionTypeEnum,
    PowerDamageTypeEnum,
    PowerFrequencyEnum,
    PowerRangeType,
    PowerSourceEnum,
    SexEnum,
    ShieldTypeEnum,
    SizeEnum,
    SkillsEnum,
    VisionEnum,
    WeaponCategoryEnum,
    WeaponGroupEnum,
    WeaponHandednessEnum,
    WeaponPropertyEnum,
)
from base.models.mixins.attacks import AttackMixin
from base.models.mixins.attributes import AttributeMixin
from base.models.mixins.defences import DefenceMixin
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

    name = models.CharField(verbose_name='Название', max_length=20, unique=True)
    prof_bonus = models.SmallIntegerField(verbose_name='Бонус владения', default=2)
    group = MultiSelectField(
        verbose_name='Группа оружия',
        choices=WeaponGroupEnum.generate_choices(),
    )
    category = models.CharField(
        verbose_name='Категория',
        choices=WeaponCategoryEnum.generate_choices(),
        max_length=WeaponCategoryEnum.max_length(),
    )
    dice_number = models.SmallIntegerField(verbose_name='Количество кубов', default=1)
    damage_dice = models.CharField(
        verbose_name='Кость урона',
        choices=DiceEnum.generate_choices(is_sorted=False),
        max_length=DiceEnum.max_length(),
    )
    properties = MultiSelectField(
        verbose_name='Свойства',
        choices=WeaponPropertyEnum.generate_choices(),
        null=True,
        blank=True,
    )
    handedness = models.CharField(
        verbose_name='Одноручное/Двуручное',
        choices=WeaponHandednessEnum.generate_choices(is_sorted=False),
        max_length=WeaponHandednessEnum.max_length(),
        default=WeaponHandednessEnum.ONE.name,
    )
    range = models.SmallIntegerField(verbose_name='Дальность', default=0)

    def __str__(self):
        return self.name

    @property
    def max_range(self):
        return self.range * 2

    def damage(self, weapon_number=1):
        return f'{self.dice_number*weapon_number}{self.get_damage_dice_display()}'


class Weapon(models.Model):
    class Meta:
        verbose_name = 'Оружие'
        verbose_name_plural = 'Оружие'

    weapon_type = models.ForeignKey(
        WeaponType, verbose_name='Тип оружия', on_delete=models.CASCADE, null=False
    )
    name = models.CharField(verbose_name='Название', max_length=20)
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)

    def __str__(self):
        if self.name == self.weapon_type.name:
            return f'{self.name}, +{self.enchantment}'
        return f'{self.name}, {self.weapon_type}, +{self.enchantment}'


class ImplementType(models.Model):
    class Meta:
        verbose_name = 'Тип инструмента'
        verbose_name_plural = 'Типы инструментов'

    name = models.CharField(verbose_name='Название', max_length=20, blank=True)
    inherited_weapon_type = models.OneToOneField(
        WeaponType,
        verbose_name='На основании оружия',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='implement_type',
    )

    def __str__(self):
        return self.name


class Implement(models.Model):
    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'

    implement_type = models.ForeignKey(
        ImplementType, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(verbose_name='Название', max_length=20)
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)

    def __str__(self):
        if self.name == self.implement_type.name:
            return f'{self.name}, +{self.enchantment}'
        return f'{self.name}, {self.implement_type}, +{self.enchantment}'


class Race(models.Model):
    class Meta:
        verbose_name = 'Раса'
        verbose_name_plural = 'Расы'

    name = models.CharField(
        verbose_name='Название',
        max_length=NPCRaceEnum.max_length(),
        choices=NPCRaceEnum.generate_choices(),
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

    available_weapon_types = models.ManyToManyField(
        WeaponType, verbose_name='Владение оружием', blank=True
    )

    def __str__(self):
        return NPCRaceEnum[self.name].value


class RaceBonus(models.Model):
    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'

    name = models.CharField(verbose_name='Название', max_length=30, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='bonuses')

    def __str__(self):
        return f'Бонус расы: {self.race.get_name_display()}'


class Class(models.Model):
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    name = models.CharField(
        verbose_name='Название',
        max_length=NPCClassEnum.max_length(),
        choices=NPCClassEnum.generate_choices(),
        unique=True,
    )
    power_source = models.CharField(
        verbose_name='Источник силы',
        choices=PowerSourceEnum.generate_choices(),
        max_length=PowerSourceEnum.max_length(),
        null=True,
    )
    subclasses = models.SmallIntegerField(
        verbose_name='Количество подклассов', default=0
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
    available_weapon_categories = MultiSelectField(
        verbose_name='Владение категориями оружия',
        choices=WeaponCategoryEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )
    available_weapon_types = models.ManyToManyField(
        WeaponType, verbose_name='Владение оружием', blank=True
    )
    available_implement_types = models.ManyToManyField(
        ImplementType, verbose_name='Доступные инструменты', blank=True
    )
    weapon_attack_attributes = MultiSelectField(
        verbose_name='Атакующие характеристики (оружие)',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        default=AttributesEnum.STRENGTH.name,
    )
    implement_attack_attributes = MultiSelectField(
        verbose_name='Атакующие характеристики (инструмент)',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )
    hit_points_per_level = models.PositiveSmallIntegerField(
        verbose_name='Хитов за уровень', default=8
    )

    def __str__(self):
        return NPCClassEnum[self.name].value


class ClassBonus(models.Model):
    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'

    name = models.CharField(verbose_name='Название', max_length=30, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    klass = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='bonuses')

    def __str__(self):
        return f'Классовое умение: {self.klass.get_name_display()}'


class Power(models.Model):
    class Meta:
        verbose_name = 'Талант'
        verbose_name_plural = 'Таланты'

    name = models.CharField(verbose_name='Название', max_length=20)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    frequency = models.CharField(
        verbose_name='Частота использования',
        choices=PowerFrequencyEnum.generate_choices(is_sorted=False),
        max_length=PowerFrequencyEnum.max_length(),
    )
    action_type = models.CharField(
        verbose_name='Действие',
        choices=PowerActionTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerActionTypeEnum.max_length(),
        default=PowerActionTypeEnum.STANDARD.name,
    )
    klass = models.ForeignKey(
        Class,
        related_name='powers',
        verbose_name='Класс',
        on_delete=models.CASCADE,
        null=False,
    )
    attack_attribute = models.CharField(
        verbose_name='Атакующая характеристика',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        default=AttributesEnum.STRENGTH.name,
        max_length=AttributesEnum.max_length(),
    )
    attack_bonus = models.SmallIntegerField(verbose_name='Бонус атаки', default=0)
    defence = models.CharField(
        verbose_name='Против защиты',
        choices=DefenceTypeEnum.generate_choices(is_sorted=False),
        max_length=DefenceTypeEnum.max_length(),
        default=DefenceTypeEnum.ARMOR_CLASS.name,
    )
    damage_type = MultiSelectField(
        verbose_name='Тип урона',
        choices=PowerDamageTypeEnum.generate_choices(),
        default=PowerDamageTypeEnum.NONE.name,
    )
    dice_number = models.SmallIntegerField(verbose_name='Количество кубов', default=1)
    damage_dice = models.CharField(
        verbose_name='Кость урона',
        null=True,
        blank=True,
        choices=DiceEnum.generate_choices(is_sorted=False),
        max_length=DiceEnum.max_length(),
    )
    accessory_type = models.CharField(
        verbose_name='Тип вооружения',
        choices=AccessoryTypeEnum.generate_choices(),
        max_length=AccessoryTypeEnum.max_length(),
    )
    range_type = models.CharField(
        verbose_name='Дальность',
        choices=PowerRangeType.generate_choices(is_sorted=False),
        max_length=PowerRangeType.max_length(),
        default=PowerRangeType.MELEE_WEAPON,
    )
    range = models.SmallIntegerField(verbose_name='Дальность', default=1)
    burst = models.SmallIntegerField(verbose_name='Площадь', default=0)
    hit_effect = models.TextField(verbose_name='Попадание', null=True, blank=True)
    miss_effect = models.TextField(verbose_name='Промах', null=True, blank=True)
    effect = models.TextField(verbose_name='Эффект', null=True, blank=True)
    parent_power = models.ForeignKey(
        'self',
        verbose_name='Родительский талант',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}, {self.klass.get_name_display()}, {self.get_frequency_display()}'

    @property
    def damage(self):
        return f'{self.dice_number}{self.get_damage_dice_display()}'

    @property
    def attack_type(self):
        if self.range_type in (
            PowerRangeType.MELEE_WEAPON.name,
            PowerRangeType.MELEE_TOUCH.name,
            PowerRangeType.RANGED_SIGHT.name,
            PowerRangeType.RANGED_WEAPON.name,
        ):
            return self.get_range_type_display()
        if self.range_type in (
            PowerRangeType.MELEE_DISTANCE.name,
            PowerRangeType.RANGED_DISTANCE.name,
        ):
            return f'{self.get_range_type_display().split()[0]} {self.range}'
        if self.range_type in (
            PowerRangeType.CLOSE_BURST.name,
            PowerRangeType.CLOSE_BLAST.name,
        ):
            return f'{self.get_range_type_display()} {self.burst}'
        if self.range_type in (
            PowerRangeType.AREA_BURST.name,
            PowerRangeType.AREA_WALL.name,
        ):
            return (
                f'{self.get_range_type_display()} {self.burst} в пределах {self.range}'
            )
        print('1'*88)
        print(self.range_type)
        print(self)
        raise ValueError('Wrong attack type')

    @property
    def keywords(self):
        return (
            self.get_action_type_display(),
            self.get_accessory_type_display(),
            self.get_frequency_display(),
            self.attack_type,
        ) + tuple(
            PowerDamageTypeEnum[type_].value
            for type_ in self.damage_type
            if type_ != PowerDamageTypeEnum.NONE.name
        )


class NPC(DefenceMixin, AttackMixin, AttributeMixin, SkillMixin, models.Model):
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

    base_strength = models.SmallIntegerField(verbose_name='Сила (базовая)')
    base_constitution = models.SmallIntegerField(
        verbose_name='Телосложение (базовое)',
    )
    base_dexterity = models.SmallIntegerField(
        verbose_name='Ловкость (базовая)',
    )
    base_intelligence = models.SmallIntegerField(
        verbose_name='Интеллект (базовый)',
    )
    base_wisdom = models.SmallIntegerField(
        verbose_name='Мудрость (базовая)',
    )
    base_charisma = models.SmallIntegerField(
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
    weapon_attack_attributes = MultiSelectField(
        verbose_name='Атакующие характеристики (оружие)',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        default=AttributesEnum.STRENGTH.name,
    )
    implement_attack_attributes = MultiSelectField(
        verbose_name='Атакующие характеристики (инструмент)',
        choices=AttributesEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )

    weapons = models.ManyToManyField(Weapon, verbose_name='Оружие', blank=True)
    implements = models.ManyToManyField(
        Implement, verbose_name='Инструменты', blank=True
    )

    powers = models.ManyToManyField(Power, blank=True)

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
        if self.race.name == NPCRaceEnum.DRAGONBORN.name:
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
    def initiative(self):
        return self.modifier(self.dexterity) + self.half_level

    @property
    def speed(self):
        if self.armor and self.race.name != NPCRaceEnum.DWARF.name:
            penalty = self.armor.speed_penalty
        else:
            penalty = 0
        return self.race.speed - penalty

    @property
    def race_and_class_feats(self):
        return self.race.bonuses.values_list('name', flat=True).union(
            self.klass.bonuses.values_list('name', flat=True)
        )

    def powers_calculated(self):
        qs = self.powers.none()
        kwargs = (
            {
                'attack_attribute': item.name,
                'then': models.Value(
                    self.modifier(getattr(self, item.name.lower())),
                    output_field=models.SmallIntegerField(),
                ),
            }
            for item in AttributesEnum
        )
        whens = (models.When(**kws) for kws in kwargs)
        attribute_case = models.Case(*whens, output_field=models.SmallIntegerField())
        frequency_case = models.Case(
            models.When(frequency=PowerFrequencyEnum.AT_WILL, then=models.Value(1)),
            models.When(frequency=PowerFrequencyEnum.ENCOUNTER, then=models.Value(2)),
            models.When(frequency=PowerFrequencyEnum.DAYLY, then=models.Value(3)),
            output_field=models.PositiveSmallIntegerField(),
        )
        bonus = self._level_bonus + self.half_level
        for weapon in self.weapons.all():
            if self.is_weapon_proficient(weapon):
                bonus += weapon.weapon_type.prof_bonus
            qs = qs.union(
                self.powers.annotate(
                    enchantment=models.Value(
                        min(weapon.enchantment, self._magic_threshold),
                        output_field=models.SmallIntegerField(),
                    ),
                    attack_modifier=attribute_case,
                    attack=models.F('attack_modifier')
                    + models.Value(bonus, output_field=models.SmallIntegerField())
                    + models.F('enchantment'),
                    dice_num=models.Value(
                        weapon.weapon_type.dice_number,
                        output_field=models.SmallIntegerField(),
                    )
                    * models.F('dice_number'),
                    dice=models.Value(
                        weapon.weapon_type.damage_dice, output_field=models.CharField()
                    ),
                    frequency_order=frequency_case,
                ).filter(accessory_type=AccessoryTypeEnum.WEAPON.name)
            )
        for implement in self.implements.all():
            if not self.is_implement_proficient(implement):
                continue
            qs = qs.union(
                self.powers.annotate(
                    enchantment=models.Value(
                        min(implement.enchantment, self._magic_threshold),
                        output_field=models.SmallIntegerField(),
                    ),
                    attack_modifier=attribute_case,
                    attack=models.F('attack_modifier')
                    + models.Value(bonus, output_field=models.SmallIntegerField())
                    + models.F('enchantment'),
                    dice_num=models.F('dice_number'),
                    dice=models.F('damage_dice'),
                    frequency_order=frequency_case,
                ).filter(accessory_type=AccessoryTypeEnum.IMPLEMENT.name)
            )
        for weapon in self.weapons.all():
            if not hasattr(weapon.weapon_type, 'implement_type'):
                continue
            qs = qs.union(
                self.powers.annotate(
                    enchantment=models.Value(
                        min(weapon.enchantment, self._magic_threshold),
                        output_field=models.SmallIntegerField(),
                    ),
                    attack_modifier=attribute_case,
                    attack=models.F('attack_modifier')
                    + models.Value(bonus, output_field=models.SmallIntegerField())
                    + models.F('enchantment'),
                    dice_num=models.F('dice_number'),
                    dice=models.F('damage_dice'),
                    frequency_order=frequency_case,
                ).filter(accessory_type=AccessoryTypeEnum.IMPLEMENT.name)
            )
        return qs.order_by('frequency_order')


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

    @property
    def excel_url(self):
        return reverse('encounter_excel', kwargs={'pk': self.pk})
