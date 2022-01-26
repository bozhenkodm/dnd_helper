import re
from functools import cached_property
from typing import Optional, Sequence

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from multiselectfield import MultiSelectField  # type: ignore

from base.constants.constants import (
    AccessoryTypeEnum,
    ArmorTypeIntEnum,
    NPCClassEnum,
    NPCRaceEnum,
    SexEnum,
    ShieldTypeEnum,
    SkillsEnum,
)
from base.managers import WeaponTypeQuerySet
from base.models.abilities import AttributeAbstract
from base.models.magic_items import ItemAbstract
from base.models.mixins.defences import DefenceMixin
from base.models.mixins.skills import SkillMixin
from base.models.powers import Power, PowerMixin
from base.objects import npc_klasses, race_classes, weapon_types_classes
from base.objects.dice import DiceRoll
from base.objects.powers_output import PowerDisplay, PowerPropertyDisplay


class Armor(ItemAbstract):
    class Meta:
        verbose_name = 'Доспех'
        verbose_name_plural = 'Доспехи'

    armor_type = models.SmallIntegerField(
        verbose_name='Тип',
        choices=ArmorTypeIntEnum.generate_choices(),
    )
    bonus_armor_class = models.SmallIntegerField(
        verbose_name='Дополнительный класс доспеха',
        default=0,
        help_text='Для магических доспехов высоких уровней',
    )
    speed_penalty = models.SmallIntegerField(verbose_name='Штраф скорости', default=0)
    skill_penalty = models.SmallIntegerField(verbose_name='Штраф навыков', default=0)

    def __str__(self):
        return f'{self.name}, +{self.enchantment}'

    @property
    def armor_class(self):
        return self.armor_type + self.bonus_armor_class

    @property
    def name(self):
        if not self.magic_item:
            return self.get_armor_type_display()
        return f'{self.get_armor_type_display()}, {self.magic_item.name}'

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

    objects = WeaponTypeQuerySet.as_manager()

    name = models.CharField(verbose_name='Название', max_length=30)
    slug = models.CharField(verbose_name='Slug', max_length=30, unique=True)

    def __str__(self):
        return self.name

    @cached_property
    def data_instance(self):
        return weapon_types_classes.get(self.slug)()

    def damage(self, weapon_number=1):
        return (
            f'{self.data_instance.dice_number*weapon_number}'
            f'{self.data_instance.damage_dice.description}'
        )


class Weapon(ItemAbstract):
    class Meta:
        verbose_name = 'Оружие'
        verbose_name_plural = 'Оружие'
        unique_together = ('magic_item', 'level', 'weapon_type')

    weapon_type = models.ForeignKey(
        WeaponType, verbose_name='Тип оружия', on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f'{self.title}, +{self.enchantment}'

    @property
    def title(self) -> str:
        if not self.magic_item:
            return str(self.weapon_type)
        return f'{self.weapon_type}, {self.magic_item}'

    @property
    def damage(self):
        if not self.enchantment:
            return (
                f'{self.data_instance.dice_number}'
                f'{self.data_instance.damage_dice.description}'
            )
        return (
            f'{self.data_instance.dice_number}'
            f'{self.data_instance.damage_dice.description} + '
            f'{self.enchantment}'
        )

    @property
    def damage_roll(self) -> DiceRoll:
        return DiceRoll(
            rolls=self.weapon_type.data_instance.dice_number,
            dice=self.weapon_type.data_instance.damage_dice,
            addendant=self.enchantment,
        )

    @property
    def data_instance(self):
        return self.weapon_type.data_instance

    @property
    def prof_bonus(self):
        return self.data_instance.prof_bonus

    def get_attack_type(self, is_melee: bool, is_ranged: bool) -> str:
        melee_attack_type, ranged_attack_type = '', ''
        if is_melee:
            distance = 2 if self.data_instance.is_reach else 1
            melee_attack_type = f'Рукопашный {distance}'
        if is_ranged:
            ranged_attack_type = (
                f'Дальнобойный '
                f'{self.data_instance.range}/{self.data_instance.max_range}'
            )
        if is_melee and is_ranged:
            return f'{melee_attack_type} или {ranged_attack_type}'
        if is_melee:
            return melee_attack_type
        if is_ranged:
            return ranged_attack_type
        raise ValueError('Wrong attack type')


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
    is_sociable = models.BooleanField(
        verbose_name='Социальная раса',
        default=True,
        help_text='Социальные расы используются для случайной генерации NPC',
    )

    def __str__(self):
        return NPCRaceEnum[self.name].description


class Class(models.Model):
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ('name_display',)

    name = models.SlugField(
        choices=NPCClassEnum.generate_choices(is_sorted=False),
        max_length=NPCClassEnum.max_length(),
    )
    name_display = models.CharField(
        verbose_name='Название',
        max_length=NPCClassEnum.max_description_length(),
    )

    def __str__(self):
        return self.name_display


class FunctionalTemplate(models.Model):
    class Meta:
        verbose_name = 'Функциональный шаблон'
        verbose_name_plural = 'Функциональные шаблоны'
        ordering = ('title',)

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


class NPC(DefenceMixin, AttributeAbstract, SkillMixin, PowerMixin, models.Model):
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
    weapons = models.ManyToManyField(
        Weapon,
        verbose_name='Вооружение',
        blank=True,
        help_text=(
            'Имеющееся у персонажа вооружение. '
            'Если список не пустой, то оружие в руки выбирается из него.'
        ),
    )
    primary_hand = models.ForeignKey(
        Weapon,
        verbose_name='Основная рука',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_primary_hands',
    )
    secondary_hand = models.ForeignKey(
        Weapon,
        verbose_name='Вторичная рука',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_secondary_hands',
    )

    powers = models.ManyToManyField(Power, blank=True)

    def __str__(self):
        return (
            f'{self.name}'
            f'{f" ({self.functional_template}) " if self.functional_template else " "}'
            f'{self.race} {self.klass} {self.level} уровня'
        )

    # FIXME these two next methods are shitshow,
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
    def _magic_threshold(self) -> int:
        """ Магический порог (максимальный бонус от магических предметов)"""
        return (self.level - 1) // 5

    @property
    def _level_bonus(self) -> int:
        """ Условный бонус к защитам, атакам и урону для мастерских персонажей"""
        return self._magic_threshold * 2 + 1

    @property
    def max_hit_points(self) -> int:
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
    def bloodied(self) -> int:
        return self.max_hit_points // 2

    @property
    def surge(self) -> int:
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
    def surges(self) -> int:
        """Количество исцелений"""
        return self._tier + 1 + self.race_data_instance.surges_number_bonus

    @property
    def initiative(self) -> int:
        return self.dex_mod + self.half_level + self.race_data_instance.initiative

    @property
    def speed(self):
        if self.armor:
            return self.race_data_instance.speed - min(
                self.armor.speed_penalty,
                self.race_data_instance.heavy_armor_speed_penalty,
            )
        return self.race_data_instance.speed

    @property
    def weapons_in_hands(self) -> Sequence[Weapon]:
        return tuple(filter(None, (self.primary_hand, self.secondary_hand)))

    @property
    def magic_items(self) -> Sequence[ItemAbstract]:
        return tuple(
            filter(
                lambda x: x and getattr(x, 'magic_item', False),
                # TODO add the rest of magic items
                (self.primary_hand, self.secondary_hand, self.armor),  # type: ignore
            )
        )

    def is_weapon_proficient(self, weapon) -> bool:
        data_instance = weapon.data_instance
        return any(
            (
                data_instance.category
                in map(int, self.klass_data_instance.available_weapon_categories),
                type(data_instance) in self.klass_data_instance.available_weapon_types,
                type(data_instance) in self.race_data_instance.available_weapon_types,
            )
        )

    def is_implement_proficient(self, weapon) -> bool:
        return (
            type(weapon.data_instance)
            in self.klass_data_instance.available_implement_types
        )

    def is_weapon_proper_for_power(
        self, power: Power, weapon: Optional[Weapon] = None
    ) -> bool:
        weapon = weapon or self.primary_hand or self.secondary_hand
        if not weapon:
            return False
        available_weapon_types = power.available_weapon_types
        if (
            available_weapon_types.count()
            and weapon.weapon_type not in available_weapon_types.all()
        ):
            return False
        if power.accessory_type == AccessoryTypeEnum.IMPLEMENT:
            return self.is_implement_proficient(weapon)
        if (
            power.accessory_type == AccessoryTypeEnum.WEAPON
            and power.accessory_type
            in (AccessoryTypeEnum.WEAPON, AccessoryTypeEnum.TWO_WEAPONS)
        ):
            # pure implements can't be used with weapon powers
            return not weapon.data_instance.is_pure_implement
        return False

    @property
    def inventory_text(self):
        return list(
            filter(
                None,
                list(
                    str(weapon)
                    for weapon in (self.weapons.all() or self.weapons_in_hands)
                )
                + [str(self.armor)]
                + [self.get_shield_display()],
            )
        )

    def parse_string(
        self,
        power: Power,
        string: str,
        weapon: Optional[Weapon] = None,
        secondary_weapon: Optional[Weapon] = None,
        item: Optional[ItemAbstract] = None,
    ):
        pattern = r'\$(\S{3,})\b'  # gets substring from '$' to next whitespace
        expressions_to_calculate = re.findall(pattern, string)
        template = re.sub(
            pattern, '{}', string
        )  # preparing template for format() method
        calculated_expressions = []
        # calculating without operations order for now, just op for op
        for expression in expressions_to_calculate:
            calculated_expressions.append(
                self.evaluate_power_expression(
                    string=expression,
                    power=power,
                    weapon=weapon,
                    secondary_weapon=secondary_weapon,
                    item=item,
                )
            )
        result = template.format(*calculated_expressions)
        # TODO remove injection weakness, leaving only markdown tags
        return mark_safe('<br>'.join(result.split('\n')))

    def powers_calculated(self):
        """
        calculated powers for npc html page
        """
        powers_qs = self.race.powers.filter(level=0)
        powers_qs |= self.powers.filter(
            models.Q(accessory_type__isnull=True) | models.Q(accessory_type='')
        )
        if self.functional_template:
            powers_qs |= self.functional_template.powers.filter(level=0)

        powers = []
        for power in powers_qs.ordered_by_frequency():
            powers.append(
                PowerDisplay(
                    name=power.name,
                    keywords=power.keywords(),
                    category=power.category(),
                    description=self.parse_string(power, string=power.description),
                    frequency_order=power.frequency_order,
                    properties=[
                        PowerPropertyDisplay(
                            title=prop.get_displayed_title(),
                            description=self.parse_string(
                                power, string=prop.get_displayed_description()
                            ),
                            debug=prop.get_displayed_description(),
                        )
                        for prop in self.valid_properties(power)
                    ],
                ).asdict()
            )
        for power in self.powers.ordered_by_frequency().filter(
            accessory_type__in=(AccessoryTypeEnum.WEAPON, AccessoryTypeEnum.IMPLEMENT)
        ):
            for weapon in self.weapons_in_hands:
                if not self.is_weapon_proper_for_power(power=power, weapon=weapon):
                    continue
                powers.append(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords(weapon),
                        category=power.category(weapon),
                        description=self.parse_string(power, power.description),
                        frequency_order=power.frequency_order,
                        properties=[
                            PowerPropertyDisplay(
                                **{
                                    'title': prop.get_displayed_title(),
                                    'description': self.parse_string(
                                        power,
                                        string=prop.get_displayed_description(),
                                        weapon=weapon,
                                    ),
                                    'debug': prop.description,
                                }
                            )
                            for prop in self.valid_properties(power)
                        ],
                    ).asdict()
                )
        for item in self.magic_items:
            for power in item.magic_item.powers.ordered_by_frequency():
                powers.append(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords(),
                        category=power.category(),
                        description=self.parse_string(power, power.description),
                        frequency_order=power.frequency_order,
                        properties=[
                            PowerPropertyDisplay(
                                **{
                                    'title': prop.get_displayed_title(),
                                    'description': self.parse_string(
                                        power,
                                        string=prop.get_displayed_description(),
                                        item=item,
                                    ),
                                    'debug': prop.description,
                                }
                            )
                            for prop in self.valid_properties(power)
                        ],
                    ).asdict()
                )

        return sorted(powers, key=lambda x: x['frequency_order'])
