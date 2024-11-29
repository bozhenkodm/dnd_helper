import re
from functools import cached_property
from typing import Sequence

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    AccessoryTypeEnum,
    ArmorTypeIntEnum,
    NPCClassEnum,
    NPCRaceEnum,
    SexEnum,
    SkillEnum,
    WeaponCategoryIntEnum,
    WeaponHandednessEnum,
)
from base.exceptions import PowerInconsistent
from base.managers import WeaponTypeQuerySet
from base.models.abilities import Ability, NPCAbilityAbstract
from base.models.bonuses import Bonus
from base.models.defences import NPCDefenceMixin
from base.models.experience import NPCExperienceAbstract
from base.models.magic_items import (
    ItemAbstract,
    MagicArmorType,
    MagicWeaponType,
    NPCMagicItemAbstract,
)
from base.models.powers import Power, PowerMixin
from base.models.skills import NPCSkillMixin, Skill
from base.objects import npc_klasses, race_classes, weapon_types_classes
from base.objects.dice import DiceRoll
from base.objects.powers_output import PowerDisplay, PowerPropertyDisplay
from base.objects.weapon_types import WeaponType as WeaponTypeClass


class ArmorType(models.Model):
    class Meta:
        verbose_name = _('Armor type')
        verbose_name_plural = _('Armor types')

    name = models.CharField(verbose_name=_('Title'), max_length=100)
    base_armor_type = models.SmallIntegerField(
        verbose_name=_('Armor type'),
        choices=ArmorTypeIntEnum.generate_choices(),
    )
    bonus_armor_class = models.SmallIntegerField(
        verbose_name=_('Additional armor class'),
        default=0,
    )
    speed_penalty = models.SmallIntegerField(verbose_name=_('Speed penalty'), default=0)
    skill_penalty = models.SmallIntegerField(
        verbose_name=_('Skills penalty'), default=0
    )
    minimal_enhancement = models.SmallIntegerField(
        verbose_name=_('Minimal enhancement'), default=0
    )
    # TODO replace with bonus model logic when implemented
    fortitude_bonus = models.PositiveSmallIntegerField(
        verbose_name=_('Fortitude bonus'), default=0
    )
    reflex_bonus = models.PositiveSmallIntegerField(
        verbose_name=_('Reflex bonus'), default=0
    )
    will_bonus = models.PositiveSmallIntegerField(
        verbose_name=_('Will bonus'), default=0
    )

    def __str__(self) -> str:
        return f'{self.get_base_armor_type_display()}, {self.name}'

    @property
    def armor_class(self) -> int:
        return self.base_armor_type + self.bonus_armor_class

    @property
    def is_light(self) -> bool:
        return self.base_armor_type in (
            ArmorTypeIntEnum.CLOTH,
            ArmorTypeIntEnum.LEATHER,
            ArmorTypeIntEnum.HIDE,
        )


class Armor(ItemAbstract):
    class Meta:
        verbose_name = _('Armor')
        verbose_name_plural = _('Armors')

    armor_type = models.ForeignKey(
        ArmorType,
        verbose_name=_('Armor type'),
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return f'{self.name}, +{self.enhancement}'

    @property
    def armor_class(self) -> int:
        return (
            self.armor_type.base_armor_type
            + self.armor_type.bonus_armor_class
            + self.enhancement
        )

    @property
    def speed_penalty(self):
        return self.armor_type.speed_penalty

    @property
    def skill_penalty(self):
        return self.armor_type.skill_penalty

    @property
    def name(self) -> str:
        magic_item_type = (
            f', {self.magic_item_type.name}' if self.magic_item_type else ''
        )
        return (
            f'{self.armor_type.get_base_armor_type_display()} '
            f'({self.armor_type.name})'
            f'{magic_item_type}'
        )

    @property
    def is_light(self) -> bool:
        return self.armor_type.base_armor_type in (
            ArmorTypeIntEnum.CLOTH,
            ArmorTypeIntEnum.LEATHER,
            ArmorTypeIntEnum.HIDE,
        )

    @classmethod
    def create_on_base(
        cls, armor_type: ArmorType, magic_armor_type: MagicArmorType, level: int
    ):
        if (level - 1) // 5 + 1 < armor_type.minimal_enhancement:
            return
        if not cls.objects.filter(
            magic_item_type=magic_armor_type, armor_type=armor_type, level=level
        ).count():
            magic_item = cls(
                magic_item_type=magic_armor_type, armor_type=armor_type, level=level
            )
            magic_item.save()


class WeaponType(models.Model):
    class Meta:
        verbose_name = _('Weapon type')
        verbose_name_plural = _('Weapon types')

    objects = WeaponTypeQuerySet.as_manager()

    name = models.CharField(
        verbose_name=_('Title'), max_length=30, null=True, blank=True
    )
    slug = models.CharField(verbose_name='Slug', max_length=30, unique=True, blank=True)
    handedness = models.CharField(
        verbose_name=_('Handedness'),
        choices=WeaponHandednessEnum.generate_choices(is_sorted=False),
        max_length=WeaponHandednessEnum.max_length(),
        null=True,
    )
    category = models.PositiveSmallIntegerField(
        verbose_name=_('Category'),
        choices=WeaponCategoryIntEnum.generate_choices(),
    )
    primary_end = models.OneToOneField(
        "self",
        verbose_name=_('Primary end'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='secondary_end',
    )

    def __str__(self) -> str:
        # return weapon_types_classes[self.slug].name
        return self.name

    @cached_property
    def data_instance(self):
        try:
            return weapon_types_classes.get(self.slug)()
        except TypeError:
            return weapon_types_classes.get(self.slug.capitalize())()

    def damage(self, weapon_number=1) -> str:
        return (
            f'{self.data_instance.dice_number * weapon_number}'
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
        return f'{self.title}, +{self.enhancement}'

    @property
    def title(self) -> str:
        if not self.magic_item_type:
            return str(self.weapon_type)
        return f'{self.weapon_type}, {self.magic_item_type}'

    @property
    def damage(self):
        if not self.enhancement:
            return (
                f'{self.data_instance.dice_number}'
                f'{self.data_instance.damage_dice.description}'
            )
        return (
            f'{self.data_instance.dice_number}'
            f'{self.data_instance.damage_dice.description} + '
            f'{self.enhancement}'
        )

    @property
    def damage_roll(self) -> DiceRoll:
        return DiceRoll(
            rolls=self.weapon_type.data_instance.dice_number,
            dice=self.weapon_type.data_instance.damage_dice,
            addendant=self.enhancement,
        )

    @property
    def data_instance(self) -> WeaponTypeClass:
        return self.weapon_type.data_instance

    @property
    def prof_bonus(self):
        return self.data_instance.prof_bonus

    @cached_property
    def handedness(self):
        return self.weapon_type.handedness

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
        raise PowerInconsistent(_('Wrong attack type'))

    @classmethod
    def create_on_base(
        cls, weapon_type: WeaponType, magic_weapon_type: MagicWeaponType, level: int
    ):
        if not cls.objects.filter(
            magic_item_type=magic_weapon_type, weapon_type=weapon_type, level=level
        ).count():
            magic_item = cls(
                magic_item_type=magic_weapon_type, weapon_type=weapon_type, level=level
            )
            magic_item.save()


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
    bonus = models.ManyToManyField(Bonus, verbose_name=_('Bonus'), blank=True)

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


class ParagonPath(models.Model):
    class Meta:
        verbose_name = _('Paragon path')
        verbose_name_plural = _('Paragon paths')

    MIN_LEVEL = 11

    title = models.CharField(max_length=50, null=False, verbose_name=_('Title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    klass = models.ForeignKey(
        Class, on_delete=models.CASCADE, verbose_name=_('Class'), null=True, blank=True
    )
    race = models.ForeignKey(
        Race, on_delete=models.CASCADE, verbose_name=_('Race'), null=True, blank=True
    )

    def __str__(self):
        if self.klass:
            return f'{self.title} ({self.klass})'
        else:
            return f'{self.title} ({self.race})'


class NPC(
    NPCDefenceMixin,
    NPCExperienceAbstract,
    NPCAbilityAbstract,
    NPCSkillMixin,
    PowerMixin,
    NPCMagicItemAbstract,
):
    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCS'

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    creation_step = models.PositiveSmallIntegerField(default=1)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name=_('Race'))
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
    paragon_path = models.ForeignKey(
        'base.ParagonPath',
        verbose_name=_('Paragon path'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sex = models.CharField(
        max_length=SexEnum.max_length(),
        choices=SexEnum.generate_choices(is_sorted=False),
        verbose_name=_('Sex'),
    )
    level = models.PositiveSmallIntegerField(verbose_name=_('Level'), default=1)
    is_bonus_applied = models.BooleanField(
        verbose_name='Применять бонус за уровень?',
        help_text='Бонус за уровень уменьшает количество исцелений',
        default=True,
    )

    trained_skills = models.ManyToManyField(Skill, verbose_name=_('Trained skills'))
    trained_weapons = models.ManyToManyField(
        WeaponType,
        blank=True,
        verbose_name=_('Trained weapon'),
        help_text=_('Weapon training in addition to training by race and class'),
    )

    armor = models.ForeignKey(
        Armor, verbose_name=_('Armor'), null=True, on_delete=models.SET_NULL
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
        return f'{self.name} {self.race} {self.full_class_name} {self.level} уровня'

    @property
    def full_class_name(self):
        if self.paragon_path:
            return f'{self.klass} ({self.paragon_path.title})'
        if self.functional_template:
            return f'{self.klass} ({self.functional_template})'
        return self.klass

    @cached_property
    def race_data_instance(self):
        return race_classes.get(self.race.name)(npc=self)

    @cached_property
    def klass_data_instance(self):
        return npc_klasses.get(self.klass.name)(npc=self)

    @property
    def all_trained_skills(self) -> list[SkillEnum]:
        return self.klass_data_instance.mandatory_skills.enum_objects + [
            SkillEnum(skill.title) for skill in self.trained_skills.all()
        ]

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
        if self.is_bonus_applied:
            return (self.level - 1) // 5
        return 0

    @_magic_threshold.setter
    def _magic_threshold(self, value: int):
        pass

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

    def is_weapon_proficient(self, weapon: Weapon) -> bool:
        data_instance = weapon.data_instance
        return any(
            (
                data_instance.category
                in map(int, self.klass_data_instance.available_weapon_categories),
                type(data_instance) in self.klass_data_instance.available_weapon_types,
                type(data_instance) in self.race_data_instance.available_weapon_types,
                weapon.weapon_type in self.trained_weapons.all(),
            )
        )

    def is_implement_proficient(self, weapon: Weapon) -> bool:
        return any(
            (
                type(weapon.data_instance)
                in self.klass_data_instance.available_implement_types,
                weapon.weapon_type in self.trained_weapons.all(),
            )
        )

    @staticmethod
    def _is_weapon_available_for_power(power: Power, weapon: Weapon) -> bool:
        if not power.available_weapon_types.count():
            return True
        return weapon.weapon_type in power.available_weapon_types.all()

    def proper_weapons_for_power(self, power: Power) -> Sequence[tuple[Weapon]]:
        result = []
        match power.accessory_type:
            case AccessoryTypeEnum.WEAPON:
                for weapon in (self.primary_hand, self.secondary_hand):
                    if (
                        weapon
                        and self.is_weapon_proficient(weapon)
                        and self._is_weapon_available_for_power(power, weapon)
                        and not weapon.data_instance.is_pure_implement
                    ):
                        result.append((weapon,))
            case AccessoryTypeEnum.IMPLEMENT:
                for weapon in (self.primary_hand, self.secondary_hand, self.no_hand):
                    if weapon and self.is_implement_proficient(weapon):
                        result.append((weapon,))
            case AccessoryTypeEnum.TWO_WEAPONS:
                if (
                    self.primary_hand
                    and self.secondary_hand
                    and self.is_weapon_proficient(self.primary_hand)
                    and self.is_weapon_proficient(self.secondary_hand)
                    and self._is_weapon_available_for_power(power, self.primary_hand)
                    and self._is_weapon_available_for_power(power, self.secondary_hand)
                ):
                    result.append((self.primary_hand, self.secondary_hand))
        return result

    @property
    def inventory_text(self):
        return map(str, self.items)

    def parse_string(
        self,
        power: Power,
        string: str,
        weapons: Sequence[Weapon] | None = None,
        item: ItemAbstract | None = None,
    ):
        try:
            primaty_weapon = weapons[0] or weapons[2]
        except (TypeError, IndexError):
            primaty_weapon = None
        try:
            secondary_weapon = weapons[1]
        except (TypeError, IndexError):
            secondary_weapon = None
        pattern = r'\$(\S+)\b'  # gets substring from '$' to next whitespace
        # TODO fix parsing cases with ")" as a last character.
        #  Now it's unmatched by regexp
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
                    weapon=primaty_weapon,
                    secondary_weapon=secondary_weapon,
                    item=item,
                )
            )
        return template.format(*calculated_expressions)

    def powers_calculated(self) -> Sequence[dict]:
        """
        calculated powers for npc html page
        """
        powers_qs = self.race.powers.filter(level=0)
        powers_qs |= self.powers.filter(
            models.Q(accessory_type__isnull=True) | models.Q(accessory_type='')
        )
        if self.functional_template:
            powers_qs |= self.functional_template.powers.filter(level=0)

        if self.paragon_path:
            powers_qs |= self.paragon_path.powers.filter(
                level__lte=self.level, accessory_type__isnull=True
            )
        powers: list[dict] = []
        for power in powers_qs.ordered_by_frequency():
            try:
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
            except PowerInconsistent as e:
                print(f"{power} display is not created with error: {e}")
                continue
        power_weapon_qs = self.powers.ordered_by_frequency().filter(  # type: ignore
            accessory_type__isnull=False
        )
        if self.paragon_path:
            power_weapon_qs |= (
                self.paragon_path.powers.ordered_by_frequency().filter(  # type: ignore
                    accessory_type__isnull=False
                )
            )
        for power in power_weapon_qs:
            for weapons in self.proper_weapons_for_power(power):
                try:
                    powers.append(
                        PowerDisplay(
                            name=power.name,
                            keywords=power.keywords(weapons),
                            category=power.category(weapons),
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
                                            weapons=weapons,
                                        ),
                                        'debug': prop.description,
                                    }
                                )
                                for prop in self.valid_properties(power)
                            ],
                        ).asdict()
                    )
                except PowerInconsistent as e:
                    print(f"{power} display is not created with error: {e}")
                    continue

        for item in self.magic_items:
            for power in item.magic_item_type.powers.ordered_by_frequency():
                try:
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
                except PowerInconsistent as e:
                    print(f"{power} display is not created with error: {e}")
        return sorted(powers, key=lambda x: (x['frequency_order'], x['name']))
