from functools import cached_property

from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

from base.constants.base import IntDescriptionSubclassEnum
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
    SexEnum,
    ShieldTypeEnum,
    SkillsEnum,
)
from base.models.mixins.abilities import AttributeMixin
from base.models.mixins.attacks import AttackMixin
from base.models.mixins.defences import DefenceMixin
from base.models.mixins.skills import SkillMixin
from base.objects import (
    implement_types_classes,
    npc_klasses,
    race_classes,
    weapon_types_classes,
)


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
    slug = models.CharField(verbose_name='Slug', max_length=20, unique=True)

    def __str__(self):
        return self.name

    @cached_property
    def data_instance(self):
        return weapon_types_classes.get(self.slug)()

    def damage(self, weapon_number=1):
        return f'{self.dataclass_instance.dice_number*weapon_number}{self.dataclass_instance.damage_dice.description}'


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
        dataclass_instance = self.weapon_type.dataclass_instance
        if not self.enchantment:
            return f'{dataclass_instance.dice_number}{dataclass_instance.damage_dice.description}'
        return f'{dataclass_instance.dice_number}{dataclass_instance.damage_dice.description} + {self.enchantment}'


class Implement(models.Model):
    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'

    slug = models.CharField(verbose_name='Тип инструмента', max_length=20)
    name = models.CharField(verbose_name='Название', max_length=20)
    enchantment = models.SmallIntegerField(verbose_name='Улучшение', default=0)

    @property
    def implement_type(self):
        return implement_types_classes[self.slug]()

    def __str__(self):
        if self.name == self.implement_type.name:
            return f'{self.name}, +{self.enchantment}'
        return f'{self.name}, {self.implement_type.name}, +{self.enchantment}'


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

    @cached_property
    def data_instance(self):
        return race_classes.get(self.name)(npc=self)

    def __str__(self):
        return NPCRaceEnum[self.name].value


class Class(models.Model):
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    name = models.SmallIntegerField(
        verbose_name='Название', choices=NPCClassIntEnum.generate_choices(), unique=True
    )
    available_shield_types = MultiSelectField(
        verbose_name='Ношение щитов',
        choices=ShieldTypeEnum.generate_choices(),
        blank=True,
        null=True,
    )

    def __str__(self):
        return NPCClassIntEnum(self.name).description

    @cached_property
    def data_instance(self):
        return npc_klasses.get(self.name)(npc=self)


class FunctionalTemplate(models.Model):
    class Meta:
        verbose_name = 'Функциональный шаблон'
        verbose_name_plural = 'Функциональные шаблоны'

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


class PowerTarget(models.Model):
    class Meta:
        verbose_name = 'Цель таланта'
        verbose_name_plural = 'Цели талантов'

    target = models.CharField(
        verbose_name='Цель', null=False, max_length=50, unique=True
    )

    def __str__(self):
        return self.target


class Power(models.Model):
    class Meta:
        verbose_name = 'Талант'
        verbose_name_plural = 'Таланты'

    name = models.CharField(verbose_name='Название', max_length=100)
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
        null=True,
        blank=False,
    )
    klass = models.ForeignKey(
        Class,
        related_name='powers',
        verbose_name='Класс',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    subclass = models.SmallIntegerField(
        verbose_name='Подкласс',
        choices=IntDescriptionSubclassEnum.generate_choices(),
        default=0,
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
        default=PowerRangeTypeEnum.PERSONAL.name,
    )
    range = models.SmallIntegerField(verbose_name='Дальность', default=1)
    burst = models.SmallIntegerField(verbose_name='Площадь', default=0)
    hit_effect = models.TextField(verbose_name='Попадание', null=True, blank=True)
    miss_effect = models.TextField(verbose_name='Промах', null=True, blank=True)
    effect = models.TextField(verbose_name='Эффект', null=True, blank=True)
    trigger = models.TextField(verbose_name='Триггер', null=True, blank=True)
    requirement = models.TextField(verbose_name='Требование', null=True, blank=True)
    target = models.ForeignKey(
        PowerTarget,
        verbose_name='Цель',
        on_delete=models.SET_NULL,
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
        if self.frequency == PowerFrequencyEnum.PASSIVE.name:
            return ''
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
        return self.klass and not self.accessory_type


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
    level = models.SmallIntegerField(verbose_name='Уровень', default=0)
    subclass = models.SmallIntegerField(
        verbose_name='Подкласс',
        choices=IntDescriptionSubclassEnum.generate_choices(),
        default=0,
    )
    description = models.TextField(verbose_name='Описание')


class AttackPowerProperty(models.Model):
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
    subclass = models.SmallIntegerField(
        verbose_name='Подкласс',
        choices=IntDescriptionSubclassEnum.generate_choices(),
        default=0,
    )
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
        return (
            f'{self.name}'
            f'{f" ({self.functional_template}) " if self.functional_template else " "}'
            f'{self.race} {self.klass} {self.level} уровня'
        )

    # TODO these two next methods are shitshow, appeared to be parallel structures of race and class
    # instead of complementing models. how to integrate npc instance to these instances and initialise them
    # in race and class models respectively?

    @cached_property
    def race_data_instance(self):
        return race_classes.get(self.race.name)(npc=self)

    @cached_property
    def klass_data_instance(self):
        return npc_klasses.get(self.klass.name)(npc=self)

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
        result = (
            self.klass_data_instance.hit_points_per_level * self.level
            + self.constitution
            + self.klass_data_instance.hit_points_bonus
        )
        if self.functional_template:
            result += (
                self.functional_template.hit_points_per_level * self.level
                + self.constitution
            )
        return result

    @property
    def bloodied(self):
        return self.max_hit_points // 2

    @property
    def surge(self):
        """
        Исцеление
        """
        return self.bloodied // 2 + self.race_data_instance.healing_surge_bonus

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
        return (
            self._modifier(self.dexterity)
            + self.half_level
            + self.race_data_instance.initiative
        )

    @property
    def speed(self):
        if self.armor:
            return self.race_data_instance.speed - min(
                self.armor.speed_penalty,
                self.race_data_instance.heavy_armor_speed_penalty,
            )
        return self.race_data_instance.speed

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
                    f'{modifier}_add1': mod_value + 1,
                    f'{modifier}_add2': mod_value + 2,
                    f'{modifier}_add3': mod_value + 3,
                    f'{modifier}_add4': mod_value + 4,
                    f'{modifier}_add5': mod_value + 5,
                    f'{modifier}_add6': mod_value + 6,
                    f'{modifier}_add9': mod_value + 9,
                    f'{modifier}_add10': mod_value + 10,
                    f'{modifier}_add_halflevel': mod_value + self.half_level,
                }
            )
        kwargs.update(
            {
                'halflevel': self.half_level,
                'halflevel_add3': self.half_level + 3,
                'halflevel_add5': self.half_level + 5,
                'level_add2': self.level + 2,
            }
        )
        if weapon:
            # TODO remove injection alert
            kwargs.update(weapon=weapon)
        return (string or '').format(**kwargs)

    def powers_calculated(self):
        powers = []
        base_attack_bonus = self._level_bonus + self.half_level
        if self.functional_template:
            for power in self.functional_template.powers.all():
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
                        damage_bonus=attack_modifier
                        + (
                            self.klass_data_instance.damage_bonus(npc=self)
                            if attack_modifier
                            else 0
                        ),
                        attack=attack_modifier + base_attack_bonus + power.attack_bonus,
                        defence=power.get_defence_display(),
                        dice_number=power.dice_number,
                        dice=power.get_damage_dice_display(),
                        frequency_order=list(PowerFrequencyEnum).index(
                            PowerFrequencyEnum[power.frequency]
                        ),
                        hit_effect=self._calculate_injected_string(power.hit_effect),
                        miss_effect=self._calculate_injected_string(power.miss_effect),
                        effect=self._calculate_injected_string(
                            power.effect or power.description
                        ),
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
                    damage_bonus=attack_modifier
                    + (self.klass_data_instance.damage_bonus if attack_modifier else 0),
                    attack=attack_modifier + base_attack_bonus + power.attack_bonus,
                    defence=power.get_defence_display(),
                    dice_number=power.dice_number,
                    dice=power.get_damage_dice_display(),
                    frequency_order=list(PowerFrequencyEnum).index(
                        PowerFrequencyEnum[power.frequency]
                    ),
                    hit_effect=self._calculate_injected_string(power.hit_effect),
                    miss_effect=self._calculate_injected_string(power.miss_effect),
                    effect=self._calculate_injected_string(
                        power.effect or power.description
                    ),
                    trigger=self._calculate_injected_string(power.trigger),
                    target=power.target,
                    accessory=str(self.race),
                )
            )
        for power in self.powers.filter(accessory_type=AccessoryTypeEnum.WEAPON.name):
            attack_modifier = self._modifier(
                getattr(self, AttributeEnum[power.attack_attribute].lname)
            )
            for weapon in self.weapons.all():
                bonus = base_attack_bonus
                if self.is_weapon_proficient(weapon):
                    bonus += +weapon.weapon_type.data_instance.prof_bonus
                    bonus += self.klass_data_instance.attack_bonus(weapon=weapon)
                enchantment = min(weapon.enchantment, self._magic_threshold)
                powers.append(
                    dict(
                        name=power.name,
                        keywords=power.keywords,
                        enchantment=enchantment,
                        damage_bonus=attack_modifier
                        + self.klass_data_instance.damage_bonus,
                        attack=attack_modifier
                        + bonus
                        + enchantment
                        + power.attack_bonus,
                        defence=power.get_defence_display(),
                        dice_number=weapon.weapon_type.data_instance.dice_number
                        * power.dice_number,
                        dice=weapon.weapon_type.data_instance.damage_dice.description,
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
                        damage_bonus=attack_modifier
                        + self.klass_data_instance.damage_bonus,
                        attack=attack_modifier
                        + base_attack_bonus
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
                    not weapon.weapon_type.data_instance.is_implement
                    or weapon.weapon_type
                    not in self.klass_data_instance.available_implement_types
                ):
                    continue
                enchantment = min(weapon.enchantment, self._magic_threshold)
                powers.append(
                    dict(
                        name=power.name,
                        keywords=power.keywords,
                        enchantment=enchantment,
                        damage_bonus=attack_modifier
                        + self.klass_data_instance.damage_bonus,
                        attack=attack_modifier
                        + base_attack_bonus
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
                    damage_bonus=0,
                    attack=0,
                    defence=power.get_defence_display(),
                    dice_number=0,
                    dice='',
                    frequency_order=list(PowerFrequencyEnum).index(
                        PowerFrequencyEnum[power.frequency]
                    ),
                    hit_effect=self._calculate_injected_string(power.hit_effect),
                    miss_effect=self._calculate_injected_string(power.miss_effect),
                    effect=self._calculate_injected_string(
                        power.effect or power.description
                    ),
                    trigger=self._calculate_injected_string(power.trigger),
                    target=power.target,
                    accessory='Пассивный'
                    if power.frequency == PowerFrequencyEnum.PASSIVE.name
                    else 'Приём',
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
