import re
from functools import cached_property
from typing import Sequence

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    AccessoryTypeEnum,
    ArmorTypeIntEnum,
    NPCClassEnum,
    NPCRaceEnum,
    SexEnum,
)
from base.managers import WeaponTypeQuerySet
from base.models.abilities import Ability, NPCAbilityAbstract
from base.models.magic_items import ItemAbstract, NPCMagicItemAbstract
from base.models.mixins.defences import NPCDefenceMixin
from base.models.powers import Power, PowerMixin
from base.models.skills import NPCSkillMixin, Skill
from base.objects import npc_klasses, race_classes, weapon_types_classes
from base.objects.dice import DiceRoll
from base.objects.powers_output import PowerDisplay, PowerPropertyDisplay
from base.objects.weapon_types import WeaponType as WeaponTypeClass


class Armor(ItemAbstract):
    class Meta:
        verbose_name = _('Armor')
        verbose_name_plural = _('Armors')

    armor_type = models.SmallIntegerField(
        verbose_name=_('Armor type'),
        choices=ArmorTypeIntEnum.generate_choices(),
    )
    bonus_armor_class = models.SmallIntegerField(
        verbose_name=_('Additional armor class'),
        default=0,
        help_text=_('For high level magic armor'),
    )
    speed_penalty = models.SmallIntegerField(verbose_name=_('Speed penalty'), default=0)
    skill_penalty = models.SmallIntegerField(
        verbose_name=_('Skills penalty'), default=0
    )

    def __str__(self) -> str:
        return f'{self.name}, +{self.enchantment}'

    @property
    def armor_class(self) -> int:
        return self.armor_type + self.bonus_armor_class

    @property
    def name(self) -> str:
        if not self.magic_item_type:
            return self.get_armor_type_display()
        return f'{self.get_armor_type_display()}, {self.magic_item_type.name}'

    @property
    def is_light(self) -> bool:
        return self.armor_type in (
            ArmorTypeIntEnum.CLOTH,
            ArmorTypeIntEnum.LEATHER,
            ArmorTypeIntEnum.HIDE,
        )


class WeaponType(models.Model):
    class Meta:
        verbose_name = _('Weapon type')
        verbose_name_plural = _('Weapon types')

    objects = WeaponTypeQuerySet.as_manager()

    name = models.CharField(verbose_name=_('Title'), max_length=30)
    slug = models.CharField(verbose_name='Slug', max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name

    @cached_property
    def data_instance(self):
        try:
            return weapon_types_classes.get(self.slug)()
        except TypeError:
            return weapon_types_classes.get(self.slug.capitalize())()

    def damage(self, weapon_number=1) -> str:
        return (
            f'{self.data_instance.dice_number*weapon_number}'
            f'{self.data_instance.damage_dice.description}'
        )


class Weapon(ItemAbstract):
    class Meta:
        verbose_name = _('Weapon')
        verbose_name_plural = _('Weapon')
        unique_together = ('magic_item_type', 'level', 'weapon_type')

    weapon_type = models.ForeignKey(
        WeaponType, verbose_name=_('Weapon type'), on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f'{self.title}, +{self.enchantment}'

    @property
    def title(self) -> str:
        if not self.magic_item_type:
            return str(self.weapon_type)
        return f'{self.weapon_type}, {self.magic_item_type}'

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
    def data_instance(self) -> WeaponTypeClass:
        return self.weapon_type.data_instance

    @property
    def prof_bonus(self):
        return self.data_instance.prof_bonus

    def get_attack_type(self, is_melee: bool, is_ranged: bool) -> str:
        # TODO localization
        melee_attack_type, ranged_attack_type = '', ''
        is_melee = is_melee and self.data_instance.is_melee
        is_ranged = is_ranged and self.data_instance.is_ranged
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
        raise ValueError(_('Wrong attack type'))


class Race(models.Model):
    class Meta:
        verbose_name = _('Race')
        verbose_name_plural = _('Races')

    name = models.CharField(
        verbose_name=_('Title'),
        max_length=NPCRaceEnum.max_length(),
        choices=NPCRaceEnum.generate_choices(),
        unique=True,
    )
    name_display = models.CharField(
        verbose_name=_('Title'), max_length=NPCRaceEnum.max_description_length()
    )
    var_ability_bonus = models.ManyToManyField(
        Ability, related_name='races', verbose_name='Выборочные бонусы характеристик'
    )

    is_sociable = models.BooleanField(
        verbose_name=_('Is race social?'),
        default=True,
        help_text=_('Social races are used for random npc generation'),
    )

    def __str__(self):
        return NPCRaceEnum[self.name].description


class Class(models.Model):
    class Meta:
        verbose_name = _('Class')
        verbose_name_plural = _('Classes')
        ordering = ('name_display',)

    name = models.SlugField(
        choices=NPCClassEnum.generate_choices(is_sorted=False),
        max_length=NPCClassEnum.max_length(),
    )
    name_display = models.CharField(
        verbose_name=_('Title'),
        max_length=NPCClassEnum.max_description_length(),
    )
    trainable_skills = models.ManyToManyField(
        Skill, verbose_name='Выборочно тренируемые навыки', related_name='classes'
    )

    def __str__(self):
        return self.name_display


class FunctionalTemplate(models.Model):
    class Meta:
        verbose_name = _('Functional template')
        verbose_name_plural = _('Functional templates')
        ordering = ('title',)

    title = models.CharField(max_length=50, null=False, verbose_name=_('Title'))
    min_level = models.SmallIntegerField(verbose_name=_('Minimal level'), default=0)
    armor_class_bonus = models.SmallIntegerField(
        verbose_name=_('Armor class bonus'), default=0
    )
    fortitude_bonus = models.SmallIntegerField(
        verbose_name=_('Fortitude bonus'), default=0
    )
    reflex_bonus = models.SmallIntegerField(verbose_name=_('Reflex bonus'), default=0)
    will_bonus = models.SmallIntegerField(verbose_name=_('Will bonus'), default=0)
    save_bonus = models.SmallIntegerField(
        verbose_name=_('Saving throws bonus'), default=2
    )
    action_points_bonus = models.SmallIntegerField(
        verbose_name=_('Action points'), default=1
    )
    hit_points_per_level = models.SmallIntegerField(
        verbose_name=_('Hits per level'), default=8
    )

    def __str__(self):
        return self.title


class NPC(
    NPCDefenceMixin, NPCAbilityAbstract, NPCSkillMixin, PowerMixin, NPCMagicItemAbstract
):
    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCS'

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    creation_step = models.PositiveSmallIntegerField(default=1)
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        verbose_name=_('Race'),
    )
    klass = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name=_('Class'),
    )
    subclass = models.SmallIntegerField(
        verbose_name=_('Subclass'),
        default=0,
    )
    functional_template = models.ForeignKey(
        FunctionalTemplate,
        on_delete=models.CASCADE,
        verbose_name=_('Functional template'),
        null=True,
        blank=True,
    )
    sex = models.CharField(
        max_length=SexEnum.max_length(),
        choices=SexEnum.generate_choices(is_sorted=False),
        verbose_name=_('Sex'),
    )
    level = models.PositiveSmallIntegerField(
        verbose_name=_('Level'),
    )
    is_bonus_applied = models.BooleanField(
        verbose_name='Применять бонус за уровень?',
        help_text='Бонус за уровень уменьшает количество исцелений',
        default=True,
    )

    trained_skills = models.ManyToManyField(Skill, verbose_name=_('Trained skills'))

    armor = models.ForeignKey(
        Armor, verbose_name=_('Armor'), null=True, on_delete=models.SET_NULL
    )
    weapons = models.ManyToManyField(
        Weapon,
        verbose_name=_('Armament'),
        blank=True,
        help_text=_(
            'Armament posessed by character. '
            'If list is not empty, weapons in hands are choose from it.'
        ),
    )
    primary_hand = models.ForeignKey(
        Weapon,
        verbose_name=_('Primary hand'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_primary_hands',
    )
    secondary_hand = models.ForeignKey(
        Weapon,
        verbose_name=_('Secondary hand'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_secondary_hands',
    )
    no_hand = models.ForeignKey(
        Weapon,
        verbose_name=_('No hand implement'),
        help_text=_("Armament that doesn't take hand slot"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_no_hands',
    )

    powers = models.ManyToManyField(Power, blank=True, verbose_name=_('Powers'))

    def __str__(self):
        # TODO localization
        return (
            f'{self.name}'
            f'{f" ({self.functional_template}) " if self.functional_template else " "}'
            f'{self.race} {self.klass} {self.level} уровня'
        )

    @cached_property
    def race_data_instance(self):
        return race_classes.get(self.race.name)(npc=self)

    @cached_property
    def klass_data_instance(self):
        return npc_klasses.get(self.klass.name)(npc=self)

    @property
    def url(self):
        return reverse('npc', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return self.url

    @property
    def half_level(self):
        return self.level // 2

    @property
    def _magic_threshold(self) -> int:
        """Maximum magic item bonus"""
        return (self.level - 1) // 5

    @property
    def _level_bonus(self) -> int:
        """NPC bonus to attacks, defences and damage"""
        if self.is_bonus_applied:
            return self._magic_threshold * 2 + 1
        return 0

    @property
    def max_hit_points(self) -> int:
        if self.is_bonus_applied:
            hit_points_per_level = self.klass_data_instance.hit_points_per_level_npc
        else:
            hit_points_per_level = self.klass_data_instance.hit_points_per_level_pc
        result = (
            hit_points_per_level * self.level
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
        Healing surge value
        """
        return self.bloodied // 2 + self.race_data_instance.healing_surge_bonus

    @property
    def _tier(self):
        if self.level < 11:
            return 0
        if self.level >= 21:
            return 2
        return 1

    @property
    def surges(self) -> int:
        """Surges number"""
        result = self.race_data_instance.surges_number_bonus
        if self.is_bonus_applied:
            result += self._tier + 1
        else:
            result += self.klass_data_instance.base_surges_per_day + self.con_mod
        return result

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
    def wielded_weapons(self) -> Sequence[Weapon]:
        return tuple(
            filter(None, (self.primary_hand, self.secondary_hand, self.no_hand))
        )

    @property
    def items(self):
        return tuple(
            filter(
                None,
                (
                    self.primary_hand,
                    self.secondary_hand,
                    self.no_hand,
                    self.armor,
                    self.arms_slot,
                    self.neck_slot,
                    self.head_slot,
                    self.feet_slot,
                    self.waist_slot,
                    self.left_ring_slot,
                    self.right_ring_slot,
                    self.gloves_slot,
                ),
            )
        )

    @property
    def magic_items(self) -> Sequence[ItemAbstract]:
        return tuple(filter(lambda x: getattr(x, 'magic_item_type'), self.items))

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
        self, power: Power, weapon: Weapon | None = None
    ) -> bool:
        weapon = weapon or self.primary_hand or self.secondary_hand
        if not weapon:
            return False
        available_weapon_types = power.available_weapon_types
        # checking available weapon types match
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
            if weapon.data_instance.is_pure_implement:
                return False
            # checking match of power and weapon range type
            return True
        return False

    @property
    def inventory_text(self):
        return map(str, self.items)

    def parse_string(
        self,
        power: Power,  # TODO refactor function signature
        string: str,
        weapon: Weapon | None = None,
        secondary_weapon: Weapon | None = None,
        item: ItemAbstract | None = None,
    ):
        pattern = r'\$(\S{3,})\b'  # gets substring from '$' to next whitespace
        expressions_to_calculate = re.findall(pattern, string)
        template = re.sub(
            pattern, '{}', string
        )  # preparing template for format() method
        calculated_expressions = []
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
        return template.format(*calculated_expressions)

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
                    frequency=power.frequency.lower(),
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
            for weapon in self.wielded_weapons:
                if not self.is_weapon_proper_for_power(power=power, weapon=weapon):
                    continue
                powers.append(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords(weapon),
                        category=power.category(weapon),
                        description=self.parse_string(power, power.description),
                        frequency_order=power.frequency_order,
                        frequency=power.frequency.lower(),
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
            for power in item.magic_item_type.powers.ordered_by_frequency():
                powers.append(
                    PowerDisplay(
                        name=power.name,
                        keywords=power.keywords(),
                        category=power.category(),
                        description=self.parse_string(
                            power, power.description, item=item
                        ),
                        frequency_order=power.frequency_order,
                        frequency=power.frequency.lower(),
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
