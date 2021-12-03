import re
from dataclasses import asdict
from functools import cached_property
from typing import Union

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
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
    PowersVariables,
    SexEnum,
    ShieldTypeEnum,
    SkillsEnum,
)
from base.managers import PowerManager
from base.models.mixins.abilities import AttributeMixin
from base.models.mixins.defences import DefenceMixin
from base.models.mixins.skills import SkillMixin
from base.objects import (
    implement_types_classes,
    npc_klasses,
    race_classes,
    weapon_types_classes,
)
from base.objects.dice import DiceRoll
from base.objects.encounter import EncounterLine
from base.objects.powers_output import PowerDisplay, PowerPropertyDisplay


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
        return (
            f'{self.name},'
            f' {ArmorTypeIntEnum(self.armor_type).description},'
            f' +{self.enchantment}'
        )

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
        return (
            f'{self.dataclass_instance.dice_number*weapon_number}'
            f'{self.dataclass_instance.damage_dice.description}'
        )


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
        dataclass_instance = self.weapon_type.data_instance
        if not self.enchantment:
            return (
                f'{dataclass_instance.dice_number}'
                f'{dataclass_instance.damage_dice.description}'
            )
        return (
            f'{dataclass_instance.dice_number}'
            f'{dataclass_instance.damage_dice.description} + '
            f'{self.enchantment}'
        )

    @property
    def damage_roll(self):
        return DiceRoll(
            rolls=self.weapon_type.data_instance.dice_number,
            dice=self.weapon_type.data_instance.damage_dice,
            addendant=self.enchantment,
        )

    @property
    def prof_bonus(self):
        return self.weapon_type.data_instance.prof_bonus


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


class Power(models.Model):
    class Meta:
        verbose_name = 'Талант'
        verbose_name_plural = 'Таланты'
        # base_manager_name = 'PowerManager'

    objects = PowerManager()

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
    available_weapon_types = models.ManyToManyField(
        WeaponType,
        verbose_name='Требования к оружию',
        help_text='для талантов с оружием',
        blank=True,
    )
    range_type = models.CharField(
        verbose_name='Дальность',
        choices=PowerRangeTypeEnum.generate_choices(is_sorted=False),
        max_length=PowerRangeTypeEnum.max_length(),
        default=PowerRangeTypeEnum.PERSONAL.name,
    )
    range = models.SmallIntegerField(verbose_name='Дальность', default=0)
    burst = models.SmallIntegerField(verbose_name='Площадь', default=0)

    def __str__(self):
        if self.race:
            return f'{self.name}, {self.race.get_name_display()}'
        if self.functional_template:
            return f'{self.name}, {self.functional_template}'
        if self.klass:
            return (
                f'{self.name}, '
                f'{self.klass.get_name_display()} '
                f'({(self.get_attack_attribute_display() or "Пр")[:3]}), '
                f'{self.get_frequency_display()}, '
                f'{self.level} уровень'
            )
        return self.name

    @property
    def defence_subjanctive(self):
        if self.defence == DefenceTypeEnum.ARMOR_CLASS.name:
            return self.get_defence_display()
        return self.get_defence_display()[:-1] + 'и'

    @property
    def damage(self):
        return f'{self.dice_number}{self.get_damage_dice_display()}'

    @property
    def attack_type(self):
        # PowerRangeTypeEnum.MELEE_TOUCH.name,
        # PowerRangeTypeEnum.RANGED_SIGHT.name,
        if self.range_type in (
            PowerRangeTypeEnum.MELEE_RANGED_WEAPON.name,
            PowerRangeTypeEnum.MELEE_WEAPON.name,
            PowerRangeTypeEnum.RANGED_WEAPON.name,
            PowerRangeTypeEnum.PERSONAL.name,
        ):
            return self.get_range_type_display()
        if (
            self.range_type
            in (
                PowerRangeTypeEnum.MELEE.name,
                PowerRangeTypeEnum.RANGED.name,
            )
            and self.range
        ):
            return f'{self.get_range_type_display().split()[0]} {self.range}'
        if self.range_type == PowerRangeTypeEnum.MELEE.name:
            return f'{self.get_range_type_display()} касание'
        if self.range_type == PowerRangeTypeEnum.RANGED.name:
            return f'{self.get_range_type_display()} видимость'
        if (
            self.range_type
            in (
                PowerRangeTypeEnum.BURST.name,
                PowerRangeTypeEnum.BLAST.name,
            )
            and not self.range
        ):
            return f'Ближняя {self.get_range_type_display().lower()} {self.burst}'
        if self.range_type in (
            PowerRangeTypeEnum.BURST.name,
            PowerRangeTypeEnum.WALL.name,
        ):
            return (
                f'Зональная {self.get_range_type_display().lower()} '
                f'{self.burst} в пределах {self.range}'
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
        Power,
        verbose_name='Талант',
        null=False,
        on_delete=models.CASCADE,
        related_name='properties',
    )
    title = models.CharField(
        choices=PowerPropertyTitle.generate_choices(),
        null=True,
        blank=True,
        max_length=PowerPropertyTitle.max_length(),
    )
    level = models.SmallIntegerField(verbose_name='Уровень', default=1)
    subclass = models.SmallIntegerField(
        verbose_name='Подкласс',
        choices=IntDescriptionSubclassEnum.generate_choices(),
        default=0,
    )
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    order = models.SmallIntegerField(verbose_name='Порядок', default=0)

    def get_displayed_title(self):
        if self.title != PowerPropertyTitle.OTHER.name:
            return self.get_title_display()
        return self.description.split('.')[0]

    def get_displayed_description(self):
        if self.title != PowerPropertyTitle.OTHER.name:
            return self.description
        return '.'.join(self.description.split('.')[1:])

    def __str__(self):
        return f'{self.title} {self.description} {self.level}'


class NPC(DefenceMixin, AttributeMixin, SkillMixin, models.Model):
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

    # TODO these two next methods are shitshow,
    #  appeared to be parallel structures of race and class
    #  instead of complementing models.
    #  how to integrate npc instance to these instances and initialise them
    #  in race and class models respectively?

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
        return self._tier + 1 + self.race_data_instance.surges_number_bonus

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

    def is_weapon_proficient(self, weapon) -> bool:
        data_instance = weapon.weapon_type.data_instance
        return any(
            (
                data_instance.category
                in map(int, self.klass_data_instance.available_weapon_categories),
                type(data_instance) in self.klass_data_instance.available_weapon_types,
                type(data_instance) in self.race_data_instance.available_weapon_types,
            )
        )

    def is_implement_proficient(self, implement):
        return (
            type(implement.implement_type)
            in self.klass_data_instance.available_implement_types
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

    @property
    def power_attrs(self):
        return {
            PowersVariables.STR: self.str_mod,
            PowersVariables.CON: self.con_mod,
            PowersVariables.DEX: self.dex_mod,
            PowersVariables.INT: self.int_mod,
            PowersVariables.WIS: self.wis_mod,
            PowersVariables.CHA: self.cha_mod,
            PowersVariables.LVL: self.level,
        }

    def parse_string(
        self, string, weapon: Weapon = None, implement: Union[Weapon, Implement] = None
    ):
        pattern = r'\$([^\s]{3,})\b'  # gets substing from '$' to next whitespace
        expressions = re.findall(pattern, string)
        template = re.sub(
            pattern, '{}', string
        )  # preparing template for format() method
        calculated_expressions = []
        # calculating without operations order for now, just op for op
        # TODO fix with polish record
        # TODO rename variables!
        for expression in expressions:
            parsed_expression = re.findall(r'[a-z]{3}|[+\-*/]|[0-9]{0,2}', expression)
            current_calculated_expression = 0
            current_operation = None
            for parsed_expression_element in parsed_expression[
                :-1
            ]:  # last element is ''
                if parsed_expression_element in ('+', '-', '*', '/'):
                    current_operation = parsed_expression_element
                    continue
                if parsed_expression_element == PowersVariables.WPN:
                    if not weapon:
                        raise ValueError('У данного таланта нет оружия')
                    current_element = weapon.damage_roll.treshhold(
                        self._magic_threshold
                    )
                elif parsed_expression_element == PowersVariables.ATK:
                    current_element = (
                        self.klass_data_instance.attack_bonus(weapon)
                        # armament enchantment
                        + min(
                            max(
                                weapon and weapon.enchantment or 0,
                                implement and implement.enchantment or 0,
                            ),
                            self._magic_threshold,
                        )
                        # power attack bonus should be added
                        # to string when creating power property
                    )
                elif parsed_expression_element == PowersVariables.DMG:
                    current_element = self.klass_data_instance.damage_bonus + min(
                        max(
                            weapon and weapon.enchantment or 0,
                            implement and implement.enchantment or 0,
                        ),
                        self._magic_threshold,
                    )
                elif parsed_expression_element.isdigit():
                    current_element = int(parsed_expression_element)
                else:
                    current_element = self.power_attrs.get(parsed_expression_element)
                if current_operation == '+':
                    current_calculated_expression += current_element
                elif current_operation == '-':
                    current_calculated_expression -= current_element
                elif current_operation == '*':
                    current_calculated_expression = (
                        current_calculated_expression * current_element
                    )
                elif current_operation == '/':
                    current_calculated_expression //= current_element
                else:
                    current_calculated_expression = current_element
            calculated_expressions.append(current_calculated_expression)
        result = template.format(*calculated_expressions)
        # TODO remove injection weakness, leaving only markdown tags
        return mark_safe('<br>'.join(result.split('\n')))

    def valid_properties(self, power: Power):
        # TODO add comments, what's going on
        properties = {}
        for prop in power.properties.filter(
            level__lte=self.level, subclass__in=(self.subclass, 0)
        ).order_by('-subclass'):
            key = f'{prop.title},{prop.order}'
            if key not in properties or properties[key].level < prop.level:
                properties[key] = prop
        return sorted(properties.values(), key=lambda x: x and x.order)

    def powers_calculated(self):
        powers = []
        if self.functional_template:
            for power in self.functional_template.powers.ordered_by_frequency().filter(
                level=0
            ):
                powers.append(
                    asdict(
                        PowerDisplay(
                            name=power.name,
                            keywords=power.keywords,
                            accessory_text=self.functional_template.title,
                            description=self.parse_string(power.description),
                            frequency_order=power.frequency_order,
                            properties=[
                                PowerPropertyDisplay(
                                    **{
                                        'title': property.get_title_display(),
                                        'description': self.parse_string(
                                            property.description,
                                        ),
                                        'debug': property.description,
                                    }
                                )
                                for property in self.valid_properties(power)
                            ],
                        )
                    )
                )
        for power in self.race.powers.ordered_by_frequency().filter(level=0):
            powers.append(
                asdict(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords,
                        accessory_text=self.race.get_name_display(),
                        description=self.parse_string(power.description),
                        frequency_order=power.frequency_order,
                        properties=[
                            PowerPropertyDisplay(
                                **{
                                    'title': property.get_title_display(),
                                    'description': self.parse_string(
                                        property.description,
                                    ),
                                    'debug': property.description,
                                }
                            )
                            for property in self.valid_properties(power)
                        ],
                    )
                )
            )

        for power in self.powers.ordered_by_frequency().filter(
            accessory_type=AccessoryTypeEnum.WEAPON.name
        ):
            if power.available_weapon_types.count():
                weapon_queryset = self.weapons.filter(
                    weapon_type__in=power.available_weapon_types.all()
                )
            else:
                weapon_queryset = self.weapons.all()
            for weapon in weapon_queryset:
                powers.append(
                    asdict(
                        PowerDisplay(
                            name=power.name,
                            keywords=power.keywords,
                            accessory_text=str(weapon),
                            description=self.parse_string(power.description),
                            frequency_order=power.frequency_order,
                            properties=[
                                PowerPropertyDisplay(
                                    **{
                                        'title': property.get_title_display(),
                                        'description': self.parse_string(
                                            property.description, weapon=weapon
                                        ),
                                        'debug': property.description,
                                    }
                                )
                                for property in self.valid_properties(power)
                            ],
                        )
                    )
                )
        for power in self.powers.ordered_by_frequency().filter(
            accessory_type=AccessoryTypeEnum.IMPLEMENT.name
        ):
            for implement in self.implements.all():
                powers.append(
                    asdict(
                        PowerDisplay(
                            name=power.name,
                            keywords=power.keywords,
                            accessory_text=str(implement),
                            description=self.parse_string(power.description),
                            frequency_order=power.frequency_order,
                            properties=[
                                PowerPropertyDisplay(
                                    **{
                                        'title': property.get_displayed_title(),
                                        'description': self.parse_string(
                                            property.description, implement=implement
                                        ),
                                        'debug': property.description,
                                    }
                                )
                                for property in self.valid_properties(power)
                            ],
                        )
                    )
                )
            for weapon in self.weapons.all():
                if (
                    type(weapon.weapon_type.data_instance)
                    not in self.klass_data_instance.available_implement_types
                ):
                    continue
                powers.append(
                    asdict(
                        PowerDisplay(
                            name=power.name,
                            keywords=power.keywords,
                            accessory_text=f'{weapon} - инструмент',
                            description=self.parse_string(power.description),
                            frequency_order=power.frequency_order,
                            properties=[
                                PowerPropertyDisplay(
                                    **{
                                        'title': property.get_displayed_title(),
                                        'description': self.parse_string(
                                            property.get_displayed_description(),
                                            implement=weapon,
                                        ),
                                        'debug': property.description,
                                    }
                                )
                                for property in self.valid_properties(power)
                            ],
                        )
                    )
                )
        for power in self.powers.ordered_by_frequency().filter(
            models.Q(accessory_type__isnull=True) | models.Q(accessory_type='')
        ):
            powers.append(
                asdict(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords,
                        accessory_text='Пассивный'
                        if power.frequency == PowerFrequencyEnum.PASSIVE.name
                        else 'Приём',
                        description=self.parse_string(power.description),
                        frequency_order=power.frequency_order,
                        properties=[
                            PowerPropertyDisplay(
                                **{
                                    'title': property.get_title_display(),
                                    'description': self.parse_string(
                                        property.description
                                    ),
                                    'debug': property.description,
                                }
                            )
                            for property in self.valid_properties(power)
                        ],
                    )
                )
            )
        return sorted(powers, key=lambda x: x['frequency_order'])


class PlayerCharacters(models.Model):
    class Meta:
        verbose_name = 'Игровой персонаж'
        verbose_name_plural = 'Игровые персонажи'

    name = models.CharField(verbose_name='Имя', max_length=50)
    armor_class = models.PositiveSmallIntegerField(verbose_name='КД', null=False)
    fortitude = models.PositiveSmallIntegerField(verbose_name='Стойкость', null=False)
    reflex = models.PositiveSmallIntegerField(verbose_name='Реакция', null=False)
    will = models.PositiveSmallIntegerField(verbose_name='Воля', null=False)
    initiative = models.PositiveSmallIntegerField(verbose_name='Инициатива', default=0)
    passive_perception = models.PositiveSmallIntegerField(
        verbose_name='Пассивная внимательность', default=0
    )
    passive_insight = models.PositiveSmallIntegerField(
        verbose_name='Пассивная проницательность', default=0
    )

    def __str__(self):
        return f'{self.name}'


class Encounter(models.Model):
    class Meta:
        verbose_name = 'Сцена'
        verbose_name_plural = 'Сцены'

    short_description = models.CharField(
        max_length=30, verbose_name='Краткое описание', null=True, blank=True
    )
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    roll_for_players = models.BooleanField(
        verbose_name='Кидать инициативу за игроков?', default=False
    )
    npcs = models.ManyToManyField(NPC, verbose_name='Мастерские персонажи', blank=True)

    def __str__(self):
        if self.short_description:
            return f'Сцена {self.short_description}'
        return f'Сцена №{self.id}'

    @property
    def url(self):
        return reverse('encounter', kwargs={'pk': self.pk})

    def roll_initiative(self):
        encounter = []
        for combatant in self.combatants_pcs.all():
            combatant: PlayerCharacters
            initiative = combatant.initiative
            if self.roll_for_players:
                initiative += DiceIntEnum.D20.roll()
            encounter.append(
                EncounterLine(
                    name=combatant.pc.name,
                    initiative=initiative,
                    ac=combatant.pc.armor_class,
                    fortitude=combatant.pc.fortitude,
                    reflex=combatant.pc.reflex,
                    will=combatant.pc.will,
                    is_player=True,
                    number=0,
                )
            )
        for npc in self.npcs.all():
            encounter.append(
                EncounterLine(
                    name=npc.name,
                    initiative=npc.initiative + DiceIntEnum.D20.roll(),
                    ac=npc.armor_class,
                    fortitude=npc.fortitude,
                    reflex=npc.reflex,
                    will=npc.will,
                    is_player=False,
                    number=0,
                )
            )
        for combatant in self.combatants.all():
            initiative = combatant.initiative + DiceIntEnum.D20.roll()
            for i in range(combatant.number):
                encounter.append(
                    EncounterLine(
                        name=combatant.name,
                        initiative=initiative,
                        ac=combatant.armor_class,
                        fortitude=combatant.fortitude,
                        reflex=combatant.reflex,
                        will=combatant.will,
                        is_player=False,
                        number=i + 1,
                    )
                )
        return sorted(
            encounter,
            key=lambda x: (x.initiative, not x.is_player, x.name),
            reverse=True,
        )


class Combatants(models.Model):
    name = models.CharField(verbose_name='Участник сцены', max_length=50, null=False)
    encounter = models.ForeignKey(
        Encounter,
        verbose_name='Сцена',
        on_delete=models.CASCADE,
        null=True,
        related_name='combatants',
    )
    armor_class = models.PositiveSmallIntegerField(verbose_name='КД', default=0)
    fortitude = models.PositiveSmallIntegerField(verbose_name='Стойкость', default=0)
    reflex = models.PositiveSmallIntegerField(verbose_name='Реакция', default=0)
    will = models.PositiveSmallIntegerField(verbose_name='Воля', default=0)
    initiative = models.PositiveSmallIntegerField(verbose_name='Инициатива', default=0)
    number = models.PositiveSmallIntegerField(
        verbose_name='Количество однотипных', default=1
    )

    def __str__(self):
        return self.name


class CombatantsPC(models.Model):
    pc = models.ForeignKey(
        PlayerCharacters, verbose_name='Игровой персонаж', on_delete=models.CASCADE
    )
    encounter = models.ForeignKey(
        Encounter,
        verbose_name='Сцена',
        on_delete=models.CASCADE,
        null=True,
        related_name='combatants_pcs',
    )
    initiative = models.PositiveSmallIntegerField(verbose_name='Инициатива', default=0)
