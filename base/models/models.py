from typing import Iterable, Sequence

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    AccessoryTypeEnum,
    NPCClassEnum,
    NPCOtherProperties,
    NPCRaceEnum,
    SexEnum,
    SizeIntEnum,
    VisionEnum,
    WeaponCategoryIntEnum,
)
from base.exceptions import PowerInconsistent, WrongWeapon
from base.models.abilities import Ability, NPCAbilityAbstract
from base.models.abstract import ConstraintAbstract
from base.models.bonuses import BonusMixin
from base.models.books import BookSource
from base.models.defences import NPCDefenceMixin
from base.models.experience import NPCExperienceAbstract
from base.models.feats import NPCFeatAbstract
from base.models.items import (
    Armor,
    ItemAbstract,
    MagicItemType,
    NPCMagicItemAbstract,
    Weapon,
    WeaponType,
)
from base.models.klass import Class, NPCClassAbstract
from base.models.powers import Power, PowerMixin
from base.models.skills import NPCSkillAbstract


class Race(models.Model):
    class Meta:
        verbose_name = _('Race')
        verbose_name_plural = _('Races')
        ordering = ('name_display',)

    name = models.CharField(
        verbose_name=_('Title'),
        max_length=NPCRaceEnum.max_length(),
        choices=NPCRaceEnum.generate_choices(),
        unique=True,
    )
    name_display = models.CharField(
        verbose_name=_('Title'), max_length=NPCRaceEnum.max_description_length()
    )
    const_ability_bonus = models.ManyToManyField(
        Ability,
        related_name='races_with_const_ability',
        verbose_name=_('Constant ability bonuses'),
    )
    var_ability_bonus = models.ManyToManyField(
        Ability,
        related_name='races',
        verbose_name=_('Selective ability bonus'),
    )
    speed = models.PositiveSmallIntegerField(verbose_name=_('Speed'), default=6)
    vision = models.CharField(
        verbose_name=_('Vision'),
        choices=VisionEnum.generate_choices(is_sorted=False),
        max_length=VisionEnum.max_length(),
        default=VisionEnum.NORMAL.value,
    )
    size = models.SmallIntegerField(
        verbose_name=_('Size'),
        choices=SizeIntEnum.generate_choices(),
        default=SizeIntEnum.MEDIUM.value,
    )
    weapon_types = models.ManyToManyField(
        WeaponType,
        verbose_name=_('Available weapon types'),
    )
    is_social = models.BooleanField(
        verbose_name=_('Is race social?'),
        default=True,
        help_text=_('Social races are used for random npc generation'),
    )
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name_display


class FunctionalTemplate(models.Model):
    class Meta:
        verbose_name = _('Functional template')
        verbose_name_plural = _('Functional templates')
        ordering = ('title',)

    title = models.CharField(max_length=50, null=False, verbose_name=_('Title'))
    min_level = models.SmallIntegerField(
        verbose_name=_('Minimal level'), default=1, choices=((1, 1), (11, 11), (21, 21))
    )
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
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class ParagonPath(ConstraintAbstract):
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
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.klass:
            return f'{self.title} ({self.klass})'
        elif self.race:
            return f'{self.title} ({self.race})'
        return self.title


class NPC(
    NPCClassAbstract,
    NPCDefenceMixin,
    NPCExperienceAbstract,
    NPCAbilityAbstract,
    NPCSkillAbstract,
    PowerMixin,
    NPCMagicItemAbstract,
    BonusMixin,
    NPCFeatAbstract,
):
    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCS'

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name=_('Race'))
    functional_template = models.ForeignKey(
        FunctionalTemplate,
        on_delete=models.CASCADE,
        verbose_name=_('Functional template'),
        null=True,
        blank=True,
    )
    paragon_path = models.ForeignKey(
        ParagonPath,
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

    armor = models.ForeignKey(
        Armor,
        verbose_name=_('Armor'),
        null=True,
        on_delete=models.SET_NULL,
        # limit_choices_to=models.Q(armor_type__base_armor_type__in=models.F('npc__klass__armor_types'))
        # | models.Q(armor_type_base_armor_type__in=models.F('subclass__armor_types')),
    )
    primary_hand = models.ForeignKey(
        Weapon,
        verbose_name=_('Primary hand'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_primary_hands',
        limit_choices_to=~models.Q(weapon_type__handedness__is_one_handed__isnull=True),
    )
    secondary_hand = models.ForeignKey(
        Weapon,
        verbose_name=_('Secondary hand'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_secondary_hands',
        limit_choices_to=~models.Q(weapon_type__handedness__is_one_handed__isnull=True),
    )
    no_hand = models.ForeignKey(
        Weapon,
        verbose_name=_('No hand implement'),
        help_text=_("Armament that doesn't take hand slot"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='in_no_hands',
        limit_choices_to={'weapon_type__handedness__is_one_handed__isnull': True},
    )

    powers = models.ManyToManyField(
        Power, blank=True, verbose_name=_('Powers'), related_name='npcs'
    )

    def __str__(self):
        # TODO localization
        return f'{self.name} {self.race} {self.full_class_name} {self.level} уровня'

    @property
    def full_class_name(self) -> str:
        if self.paragon_path:
            return f'{self.klass} ({self.paragon_path.title})'
        if self.functional_template:
            return f'{self.klass} ({self.functional_template})'
        return str(self.klass)

    @property
    def url(self) -> str:
        return reverse('npc', kwargs={'pk': self.pk})

    def get_absolute_url(self) -> str:
        return self.url

    @property
    def half_level(self) -> int:
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
            hit_points_per_level = self.klass.hit_points_per_level_npc
        else:
            hit_points_per_level = self.klass.hit_points_per_level
        result = (
            hit_points_per_level * self.level
            + self.constitution
            + self.calculate_bonus(NPCOtherProperties.HIT_POINTS)
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
        return self.bloodied // 2 + self.calculate_bonus(NPCOtherProperties.SURGE)

    @property
    def _tier(self) -> int:
        if self.level < 11:
            return 0
        if self.level >= 21:
            return 2
        return 1

    @property
    def surges(self) -> int:
        """Surges number"""
        result = self.calculate_bonus(NPCOtherProperties.SURGES)
        if self.is_bonus_applied:
            result += self._tier + 1
        else:
            result += self.klass.surges + self.con_mod
        return result

    @property
    def damage_bonus(self) -> int:
        base_bonus = self._level_bonus
        if self.klass.name != NPCClassEnum.HEXBLADE:
            return base_bonus
        damage_modifier = 0
        if self.subclass.slug in (
            'FEY_PACT',
            'GLOOM_PACT',
        ):
            damage_modifier = self.dex_mod
        if self.subclass.slug in (
            'INFERNAL_PACT',
            'ELEMENTAL_PACT',
        ):
            damage_modifier = self.con_mod
        if self.subclass.slug == 'STAR_PACT':
            damage_modifier = self.int_mod
        return base_bonus + ((self.level - 5) // 10 * 2 + 2 + damage_modifier)

    @property
    def initiative(self) -> int:
        return (
            self.dex_mod
            + self.half_level
            + self.calculate_bonus(NPCOtherProperties.INITIATIVE)
        )

    @property
    def speed(self) -> int:
        bonus_speed = self.calculate_bonus(NPCOtherProperties.SPEED)
        if self.armor and self.race.name != NPCRaceEnum.DWARF:
            return self.race.speed + self.armor.speed_penalty + bonus_speed
        return self.race.speed + bonus_speed

    @property
    def items(self) -> tuple[ItemAbstract, ...]:
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

    @property
    def magic_item_types(self) -> Sequence[MagicItemType]:
        return tuple(item.magic_item_type for item in self.magic_items)

    def is_weapon_proficient(self, weapon: Weapon) -> bool:
        return any(
            (
                weapon.category in self.klass.weapon_categories.all(),
                weapon.category in self.subclass.weapon_categories.all(),
                weapon.weapon_type in self.klass.weapon_types.all(),
                weapon.weapon_type in self.subclass.weapon_types.all(),
                weapon.weapon_type in self.race.weapon_types.all(),
                weapon.weapon_type in self.trained_weapons.all(),
            )
        )

    def is_implement_proficient(self, weapon: Weapon) -> bool:
        return any(
            (
                weapon.weapon_type in self.klass.implement_types.all(),
                weapon.weapon_type in self.trained_weapons.all(),
            )
        )

    @staticmethod
    def _is_weapon_available_for_power(power: Power, weapon: Weapon) -> bool:
        if not power.weapon_types.all():
            return True
        return weapon.weapon_type in power.weapon_types.all()

    def proper_weapons_for_power(self, power: Power) -> Sequence[tuple[Weapon, ...]]:
        result: list[tuple[Weapon, ...]] = []
        match power.accessory_type:
            case None:
                return [()]
            case AccessoryTypeEnum.WEAPON:
                for weapon in filter(None, (self.primary_hand, self.secondary_hand)):
                    if (
                        weapon
                        and self.is_weapon_proficient(weapon)
                        and self._is_weapon_available_for_power(power, weapon)
                        and weapon.weapon_type.category.code
                        != WeaponCategoryIntEnum.IMPLEMENT
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
    def inventory_text(self) -> Iterable[str]:
        return map(str, self.items)

    def all_powers_qs(self) -> models.QuerySet[Power]:
        query = (
            models.Q(race=self.race, level=0)
            | models.Q(npcs=self)
            | models.Q(classes=self.klass, level__lte=self.level)
            | models.Q(subclasses=self.subclass, level__lte=self.level)
            | models.Q(magic_item_type__in=self.magic_item_types)
        )
        if self.functional_template:
            query |= models.Q(
                functional_template=self.functional_template,
            )
        if self.paragon_path:
            query |= models.Q(paragon_path=self.paragon_path)
        # TODO get rid of distinct
        return Power.objects.filter(query).distinct().order_by('frequency', 'name')

    def powers_calculate(
        self, powers_qs: Sequence[Power] | None = None
    ) -> Sequence[dict]:
        """
        calculated powers for npc html page
        """
        powers_qs = powers_qs or self.all_powers_qs()
        powers: list[dict] = []
        for power in powers_qs:
            if not power.magic_item_type:
                for weapons in self.proper_weapons_for_power(power):
                    try:
                        powers.append(
                            self.get_power_display(power=power, weapons=weapons)
                        )
                    except PowerInconsistent as e:
                        print(f"{power} display is not created with error: {e}")
                        powers.append(self.get_power_inconsistent_message(power))
                        continue
                    except WrongWeapon as e:
                        print(f"{power} display is not created with error: {e}")
                        continue
                continue
            for item in self.magic_items:
                if power.magic_item_type != item.magic_item_type:
                    continue
                try:
                    powers.append(self.get_power_display(power=power, item=item))
                except PowerInconsistent as e:
                    print(f"{power} display is not created with error: {e}")
                    powers.append(self.get_power_inconsistent_message(power))
        return powers

    def powers_calculated(self) -> Sequence[dict]:
        if result := cache.get(self._powers_cache_key):
            return result
        return self.powers_calculate()

    def cache_all(self):
        self.cache_bonuses()
        self.cache_powers()
