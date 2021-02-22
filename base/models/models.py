from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

from base.constants.constants import (
    AccessoryTypeEnum,
    ArmorTypeIntEnum,
    AttributeEnum,
    DefenceTypeEnum,
    DiceIntEnum,
    NPCClassIntEnum,
    NPCRaceEnum,
    PowerActionTypeEnum,
    PowerDamageTypeEnum,
    PowerEffectTypeEnum,
    PowerFrequencyEnum,
    PowerPropertyTitle,
    PowerRangeTypeEnum,
    PowerSourceEnum,
    SexEnum,
    ShieldTypeEnum,
    SizeEnum,
    SkillsEnum,
    VisionEnum,
    WeaponCategoryIntEnum,
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
    armor_type = models.SmallIntegerField(
        verbose_name='Тип',
        choices=ArmorTypeIntEnum.generate_choices(),
    )
    armor_class = models.SmallIntegerField(verbose_name='Класс доспеха', default=0)
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)
    speed_penalty = models.SmallIntegerField(verbose_name='Штраф скорости', default=0)
    skill_penalty = models.SmallIntegerField(verbose_name='Штраф навыков', default=0)

    def __str__(self):
        if self.name == ArmorTypeIntEnum(self.armor_type).description:
            return f'{self.name}, +{self.enchantment}'
        return f'{self.name}, {ArmorTypeIntEnum(self.armor_type).description}, +{self.enchantment}'

    @property
    def is_light(self):
        return self.armor_type in (
            ArmorTypeIntEnum.CLOTH,
            ArmorTypeIntEnum.LEATHER,
            ArmorTypeIntEnum.HIDE,
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
    category = models.SmallIntegerField(
        verbose_name='Категория',
        choices=WeaponCategoryIntEnum.generate_choices(),
    )
    dice_number = models.SmallIntegerField(verbose_name='Количество кубов', default=1)
    damage_dice = models.SmallIntegerField(
        verbose_name='Кость урона',
        choices=DiceIntEnum.generate_choices(),
        null=True,
        blank=True,
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

    @property
    def damage(self):
        if not self.enchantment:
            return f'{self.weapon_type.dice_number}{self.weapon_type.get_damage_dice_display()}'
        return f'{self.weapon_type.dice_number}{self.weapon_type.get_damage_dice_display()} + {self.enchantment}'


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
        choices=AttributeEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    var_bonus_attrs = MultiSelectField(
        verbose_name='Выборочные бонусы характеристик',
        choices=AttributeEnum.generate_choices(is_sorted=False),
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

    name = models.SmallIntegerField(
        verbose_name='Название', choices=NPCClassIntEnum.generate_choices(), unique=True
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
        choices=ArmorTypeIntEnum.generate_choices(),
        default=ArmorTypeIntEnum.CLOTH.value,
    )
    available_shield_types = MultiSelectField(
        verbose_name='Ношение щитов',
        choices=ShieldTypeEnum.generate_choices(),
        blank=True,
        null=True,
    )
    available_weapon_categories = MultiSelectField(
        verbose_name='Владение категориями оружия',
        choices=WeaponCategoryIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    available_weapon_types = models.ManyToManyField(
        WeaponType, verbose_name='Владение оружием', blank=True
    )
    available_implement_types = models.ManyToManyField(
        ImplementType, verbose_name='Доступные инструменты', blank=True
    )
    hit_points_per_level = models.PositiveSmallIntegerField(
        verbose_name='Хитов за уровень', default=8
    )

    def __str__(self):
        return NPCClassIntEnum(self.name).description


class ClassBonus(models.Model):
    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'

    name = models.CharField(verbose_name='Название', max_length=30, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    klass = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='bonuses')

    def __str__(self):
        return f'Классовое умение: {self.klass.get_name_display()}'


class FunctionalTemplate(models.Model):
    class Meta:
        verbose_name = 'Функциональный шаблон'
        verbose_name_plural = 'Фунециональные шаблоны'

    title = models.CharField(max_length=50, null=False, verbose_name='Название')
    min_level = models.SmallIntegerField(verbose_name='Минимальный уровень', default=0)
    armor_class_bonus = models.SmallIntegerField(verbose_name='Бонус КД', default=0)
    fortitude_bonus = models.SmallIntegerField(
        verbose_name='Бонус стойкости', default=0
    )
    reflex_bonus = models.SmallIntegerField(verbose_name='Бонус реакции', default=0)
    will_bonus = models.SmallIntegerField(verbose_name='Бонус воли', default=0)
    save_bonus = models.SmallIntegerField(verbose_name='Бонус спасбросков', default=2)
    action_points_bonus = models.SmallIntegerField(
        verbose_name='Дополнительные очки действия', default=1
    )
    hit_points_per_level = models.SmallIntegerField(
        verbose_name='Хиты за уровень', default=8
    )

    def __str__(self):
        return self.title


class Power(models.Model):
    class Meta:
        verbose_name = 'Талант'
        verbose_name_plural = 'Таланты'

    name = models.CharField(verbose_name='Название', max_length=40)
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
        null=True,
        blank=True,
    )
    race = models.ForeignKey(
        Race,
        verbose_name='Раса',
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='powers',
    )
    functional_template = models.ForeignKey(
        FunctionalTemplate,
        verbose_name='Функциональный шаблон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='powers',
    )
    level = models.SmallIntegerField(verbose_name='Уровень', default=0)
    attack_attribute = models.CharField(
        verbose_name='Атакующая характеристика',
        choices=AttributeEnum.generate_choices(is_sorted=False),
        max_length=AttributeEnum.max_length(),
        null=True,
        blank=True,
    )
    attack_bonus = models.SmallIntegerField(verbose_name='Бонус атаки', default=0)
    defence = models.CharField(
        verbose_name='Против защиты',
        choices=DefenceTypeEnum.generate_choices(is_sorted=False),
        max_length=DefenceTypeEnum.max_length(),
        null=True,
        blank=True,
    )
    effect_type = MultiSelectField(
        verbose_name='Тип эффекта',
        choices=PowerEffectTypeEnum.generate_choices(),
        default=PowerEffectTypeEnum.NONE.name,
    )
    damage_type = MultiSelectField(
        verbose_name='Тип урона',
        choices=PowerDamageTypeEnum.generate_choices(),
        default=PowerDamageTypeEnum.NONE.name,
    )
    dice_number = models.SmallIntegerField(verbose_name='Количество кубов', default=1)
    damage_dice = models.SmallIntegerField(
        verbose_name='Кость урона',
        choices=DiceIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    accessory_type = models.CharField(
        verbose_name='Тип вооружения',
        choices=AccessoryTypeEnum.generate_choices(),
        max_length=AccessoryTypeEnum.max_length(),
        null=True,
        blank=True,
    )
    range_type = models.CharField(
        verbose_name='Дальность',
        choices=PowerRangeTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerRangeTypeEnum.max_length(),
        default=PowerRangeTypeEnum.MELEE_WEAPON,
    )
    range = models.SmallIntegerField(verbose_name='Дальность', default=1)
    burst = models.SmallIntegerField(verbose_name='Площадь', default=0)
    hit_effect = models.TextField(verbose_name='Попадание', null=True, blank=True)
    miss_effect = models.TextField(verbose_name='Промах', null=True, blank=True)
    effect = models.TextField(verbose_name='Эффект', null=True, blank=True)
    trigger = models.TextField(verbose_name='Триггер', null=True, blank=True)
    requirement = models.TextField(verbose_name='Требование', null=True, blank=True)
    target = models.CharField(
        verbose_name='Цель',
        null=True,
        default='Одно существо',
        max_length=50,
        blank=True,
    )

    parent_power = models.ForeignKey(
        'self',
        verbose_name='Родительский талант',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.race:
            return f'{self.name}, {self.race.get_name_display()}'
        if self.functional_template:
            return f'{self.name}, {self.functional_template}'
        return (
            f'{self.name}, '
            f'{self.klass.get_name_display()} ({(self.get_attack_attribute_display() or "Пр")[:3]}), '
            f'{self.get_frequency_display()}, '
            f'{self.level} уровень'
        )

    @property
    def damage(self):
        return f'{self.dice_number}{self.get_damage_dice_display()}'

    @property
    def attack_type(self):
        if self.range_type in (
            PowerRangeTypeEnum.MELEE_RANGED_WEAPON.name,
            PowerRangeTypeEnum.MELEE_WEAPON.name,
            PowerRangeTypeEnum.MELEE_TOUCH.name,
            PowerRangeTypeEnum.RANGED_SIGHT.name,
            PowerRangeTypeEnum.RANGED_WEAPON.name,
            PowerRangeTypeEnum.PERSONAL.name,
        ):
            return self.get_range_type_display()
        if self.range_type in (
            PowerRangeTypeEnum.MELEE_DISTANCE.name,
            PowerRangeTypeEnum.RANGED_DISTANCE.name,
        ):
            return f'{self.get_range_type_display().split()[0]} {self.range}'
        if self.range_type in (
            PowerRangeTypeEnum.CLOSE_BURST.name,
            PowerRangeTypeEnum.CLOSE_BLAST.name,
        ):
            return f'{self.get_range_type_display()} {self.burst}'
        if self.range_type in (
            PowerRangeTypeEnum.AREA_BURST.name,
            PowerRangeTypeEnum.AREA_WALL.name,
        ):
            return (
                f'{self.get_range_type_display()} {self.burst} в пределах {self.range}'
            )
        raise ValueError('Wrong attack type')

    @property
    def keywords(self):
        return filter(
            None,
            (
                self.get_action_type_display(),
                self.get_accessory_type_display() if self.accessory_type else '',
                self.get_frequency_display(),
                self.attack_type,
            )
            + tuple(
                PowerDamageTypeEnum[type_].value
                for type_ in self.damage_type
                if type_ != PowerDamageTypeEnum.NONE.name
            )
            + tuple(
                PowerEffectTypeEnum[type_].value
                for type_ in self.effect_type
                if type_ != PowerEffectTypeEnum.NONE.name
            ),
        )

    @property
    def is_utility(self):
        return not self.accessory_type


class PowerProperty(models.Model):
    power = models.ForeignKey(
        Power, verbose_name='Талант', null=False, on_delete=models.CASCADE
    )
    title = models.CharField(
        choices=PowerPropertyTitle.generate_choices(),
        null=True,
        blank=True,
        max_length=PowerPropertyTitle.max_length(),
    )
    subclass = models.SmallIntegerField(verbose_name='Подкласс', choices=(), default=0)
    description = models.TextField(verbose_name='Описание')


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
    subclass = models.SmallIntegerField(verbose_name='Подкласс', choices=(), default=0)
    functional_template = models.ForeignKey(
        FunctionalTemplate,
        on_delete=models.CASCADE,
        verbose_name='Функциональный шаблон',
        null=True,
        blank=True,
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
        max_length=AttributeEnum.max_length(),
        choices=AttributeEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )

    level4_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 4 уровне',
        choices=AttributeEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level8_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 8 уровне',
        choices=AttributeEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level14_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 14 уровне',
        choices=AttributeEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level18_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 18 уровне',
        choices=AttributeEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level24_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 24 уровне',
        choices=AttributeEnum.generate_choices(is_sorted=False),
        max_choices=2,
        null=True,
        blank=True,
    )
    level28_bonus_attrs = MultiSelectField(
        verbose_name='Бонус характеристики на 28 уровне',
        choices=AttributeEnum.generate_choices(is_sorted=False),
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
        result = self.klass.hit_points_per_level * self.level + self.constitution
        if self.klass.name == NPCClassIntEnum.RANGER_MELEE:
            result += 5 * (
                self._tier + 1
            )  # Бонусная черта крепкое тело у рейнджеров рукопашников
        if self.functional_template:
            result += self.functional_template.hit_points_per_level * self.level + self.constitution
        return result

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
            result += self._modifier(self.constitution)
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

    @property
    def initiative(self):
        return self._modifier(self.dexterity) + self.half_level

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

    @property
    def inventory_text(self):
        return list(
            filter(
                None,
                list(str(weapon) for weapon in self.weapons.all())
                + list(str(implement) for implement in self.implements.all())
                + [str(self.armor)]
                + [self.get_shield_display()],
            )
        )

    def _calculate_injected_string(self, string, weapon=None):
        kwargs = {}
        for attr in AttributeEnum:
            modifier = f'{attr.lname[:3]}_mod'
            mod_value = getattr(self, modifier)
            kwargs.update(
                {
                    modifier: getattr(self, modifier),
                    f'half_{modifier}': mod_value // 2,
                    f'{modifier}_add10': mod_value + 10,
                    f'{modifier}_add5': mod_value + 5,
                    f'{modifier}_add1': mod_value + 1,
                    f'{modifier}_add2': mod_value + 2,
                    f'{modifier}_add_halflevel': mod_value + self.half_level,
                }
            )
        kwargs.update(
            {
                'halflevel': self.half_level,
                'halflevel_add3': self.half_level + 3,
                'level_add2': self.level + 2,
            }
        )
        if weapon:
            # TODO remove injection alert
            kwargs.update(weapon=weapon)
        return (string or '').format(**kwargs)

    def _get_power_dict(self, power, attack_modifier, bonus, accessory, enchantment=0):
        return dict(
            name=power.name,
            keywords=power.keywords,
            enchantment=0,
            attack_modifier=attack_modifier,
            attack=attack_modifier + bonus + power.attack_bonus,
            defence=power.get_defence_display(),
            dice_number=power.dice_number,
            dice=power.get_damage_dice_display(),
            frequency_order=list(PowerFrequencyEnum).index(
                PowerFrequencyEnum[power.frequency]
            ),
            hit_effect=self._calculate_injected_string(power.hit_effect),
            miss_effect=self._calculate_injected_string(power.miss_effect),
            effect=self._calculate_injected_string(power.effect),
            trigger=self._calculate_injected_string(power.trigger),
            target=power.target,
            accessory=accessory,
        )

    def powers_calculated(self):
        powers = []
        base_bonus = self._level_bonus + self.half_level
        if self.functional_template:
            for power in self.functional_template.powers.all():
                attack_modifier = (
                    self._modifier(
                        getattr(self, AttributeEnum[power.attack_attribute].lname)
                    )
                    if power.attack_attribute
                    else 0
                )
                # powers.append(
                #     self._get_power_dict(
                #         power=power, attack_modifier=attack_modifier, bonus=base_bonus, accessory=self.functional_template.title, enchantment=0
                #     )
                # )
                powers.append(
                    dict(
                        name=power.name,
                        keywords=power.keywords,
                        enchantment=0,
                        attack_modifier=attack_modifier,
                        attack=attack_modifier + base_bonus + power.attack_bonus,
                        defence=power.get_defence_display(),
                        dice_number=power.dice_number,
                        dice=power.get_damage_dice_display(),
                        frequency_order=list(PowerFrequencyEnum).index(
                            PowerFrequencyEnum[power.frequency]
                        ),
                        hit_effect=self._calculate_injected_string(power.hit_effect),
                        miss_effect=self._calculate_injected_string(power.miss_effect),
                        effect=self._calculate_injected_string(power.effect),
                        trigger=self._calculate_injected_string(power.trigger),
                        target=power.target,
                        accessory=self.functional_template.title,
                    )
                )
        for power in self.race.powers.all():
            attack_modifier = (
                self._modifier(
                    getattr(self, AttributeEnum[power.attack_attribute].lname)
                )
                if power.attack_attribute
                else 0
            )
            powers.append(
                dict(
                    name=power.name,
                    keywords=power.keywords,
                    enchantment=0,
                    attack_modifier=attack_modifier,
                    attack=attack_modifier + base_bonus + power.attack_bonus,
                    defence=power.get_defence_display(),
                    dice_number=power.dice_number,
                    dice=power.get_damage_dice_display(),
                    frequency_order=list(PowerFrequencyEnum).index(
                        PowerFrequencyEnum[power.frequency]
                    ),
                    hit_effect=self._calculate_injected_string(power.hit_effect),
                    miss_effect=self._calculate_injected_string(power.miss_effect),
                    effect=self._calculate_injected_string(power.effect),
                    trigger=self._calculate_injected_string(power.trigger),
                    target=power.target,
                    accessory='Расовый',
                )
            )
        for power in self.powers.filter(accessory_type=AccessoryTypeEnum.WEAPON.name):
            attack_modifier = self._modifier(
                getattr(self, AttributeEnum[power.attack_attribute].lname)
            )
            if (
                range_type := PowerRangeTypeEnum[power.range_type]
            ).is_melee or range_type.is_close:
                filters = models.Q(
                    weapon_type__category__in=(
                        WeaponCategoryIntEnum.SIMPLE,
                        WeaponCategoryIntEnum.MILITARY,
                        WeaponCategoryIntEnum.SUPERIOR,
                    )
                )
            else:
                filters = (
                    models.Q(
                        weapon_type__category__in=(
                            WeaponCategoryIntEnum.SIMPLE_RANGED,
                            WeaponCategoryIntEnum.MILITARY_RANGED,
                            WeaponCategoryIntEnum.SUPERIOR_RANGED,
                        )
                    )
                    | models.Q(
                        weapon_type__properties__contains=WeaponPropertyEnum.LIGHT_THROWN.name
                    )
                    | models.Q(
                        weapon_type__properties__contains=WeaponPropertyEnum.HEAVY_THROWN.name
                    )
                )

            for weapon in self.weapons.filter(filters):
                bonus = base_bonus
                if self.is_weapon_proficient(weapon):
                    bonus += +weapon.weapon_type.prof_bonus
                    bonus += self.subclass_attack_bonus(weapon)
                enchantment = min(weapon.enchantment, self._magic_threshold)
                powers.append(
                    dict(
                        name=power.name,
                        keywords=power.keywords,
                        enchantment=enchantment,
                        attack_modifier=attack_modifier,
                        attack=attack_modifier
                        + bonus
                        + enchantment
                        + power.attack_bonus,
                        defence=power.get_defence_display(),
                        dice_number=weapon.weapon_type.dice_number * power.dice_number,
                        dice=weapon.weapon_type.get_damage_dice_display(),
                        frequency_order=list(PowerFrequencyEnum).index(
                            PowerFrequencyEnum[power.frequency]
                        ),
                        hit_effect=self._calculate_injected_string(
                            power.hit_effect, weapon
                        ),
                        miss_effect=self._calculate_injected_string(
                            power.miss_effect, weapon
                        ),
                        effect=self._calculate_injected_string(power.effect, weapon),
                        trigger=self._calculate_injected_string(power.trigger, weapon),
                        target=power.target,
                        accessory=str(weapon),
                    )
                )
        for power in self.powers.filter(
            accessory_type=AccessoryTypeEnum.IMPLEMENT.name
        ):
            attack_modifier = self._modifier(
                getattr(self, AttributeEnum[power.attack_attribute].lname)
            )
            for implement in self.implements.all():
                if not self.is_implement_proficient(implement):
                    continue
                enchantment = min(implement.enchantment, self._magic_threshold)
                powers.append(
                    dict(
                        name=power.name,
                        keywords=power.keywords,
                        enchantment=enchantment,
                        attack_modifier=attack_modifier,
                        attack=attack_modifier
                        + base_bonus
                        + enchantment
                        + power.attack_bonus,
                        defence=power.get_defence_display(),
                        dice_number=power.dice_number,
                        dice=power.get_damage_dice_display(),
                        frequency_order=list(PowerFrequencyEnum).index(
                            PowerFrequencyEnum[power.frequency]
                        ),
                        hit_effect=self._calculate_injected_string(power.hit_effect),
                        miss_effect=self._calculate_injected_string(power.miss_effect),
                        effect=self._calculate_injected_string(power.effect),
                        trigger=self._calculate_injected_string(power.trigger),
                        target=power.target,
                        accessory=str(implement),
                    )
                )
            for weapon in self.weapons.all():
                if (
                    not hasattr(weapon.weapon_type, 'implement_type')
                    or not self.klass.available_implement_types.filter(
                        name=weapon.weapon_type.implement_type.name
                    ).count()
                ):
                    continue
                enchantment = min(weapon.enchantment, self._magic_threshold)
                powers.append(
                    dict(
                        name=power.name,
                        keywords=power.keywords,
                        enchantment=enchantment,
                        attack_modifier=attack_modifier,
                        attack=attack_modifier
                        + base_bonus
                        + enchantment
                        + power.attack_bonus,
                        defence=power.get_defence_display(),
                        dice_number=power.dice_number,
                        dice=power.get_damage_dice_display(),
                        frequency_order=list(PowerFrequencyEnum).index(
                            PowerFrequencyEnum[power.frequency]
                        ),
                        hit_effect=self._calculate_injected_string(power.hit_effect),
                        miss_effect=self._calculate_injected_string(power.miss_effect),
                        effect=self._calculate_injected_string(power.effect),
                        trigger=self._calculate_injected_string(power.trigger),
                        target=power.target,
                        accessory=f'{weapon} - инструмент',
                    )
                )
        for power in self.powers.filter(
            models.Q(accessory_type__isnull=True) | models.Q(accessory_type='')
        ):
            powers.append(
                dict(
                    name=power.name,
                    keywords=power.keywords,
                    enchantment=0,
                    attack_modifier=0,
                    attack=0,
                    defence=power.get_defence_display(),
                    dice_number=0,
                    dice='',
                    frequency_order=list(PowerFrequencyEnum).index(
                        PowerFrequencyEnum[power.frequency]
                    ),
                    hit_effect=self._calculate_injected_string(power.hit_effect),
                    miss_effect=self._calculate_injected_string(power.miss_effect),
                    effect=self._calculate_injected_string(power.effect),
                    trigger=self._calculate_injected_string(power.trigger),
                    target=power.target,
                    accessory='Приём',
                )
            )
        return sorted(powers, key=lambda x: x['frequency_order'])


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
