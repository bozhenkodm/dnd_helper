from itertools import chain
from multiprocessing.managers import Value

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
    AbilityEnum,
    ArmamentSlot,
    ArmorTypeIntEnum,
    NPCOtherProperties,
    ShieldTypeIntEnum,
    WeaponCategoryIntEnum,
    WeaponGroupEnum, NPCClassProperties, PowerSourceIntEnum,
)
from base.models.abstract import ClassAbstract
from base.models.models import WeaponType


class Constraint(models.Model):
    class Meta:
        verbose_name = _('Constraint')
        verbose_name_plural = _('Constraints')

    name = models.CharField(verbose_name=_('Name'), max_length=100, blank=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label': 'base',
            'model__in': (
                'race',
                'class',
                'functionaltemplate',
                'paragonpath',
                'magicitemtype',
                'feat',
            ),
        },
    )
    object_id = models.PositiveIntegerField(default=0)
    belongs_to = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name or f'{self.belongs_to}'


class Condition(models.Model):
    constraint = models.ForeignKey(
        Constraint, on_delete=models.CASCADE, related_name='conditions'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label': 'base',
            'model__in': (
                'race',
                'class',
                'subclass',
                'functionaltemplate',
                'paragonpath',
                'feat',
                'power',
            ),
        },
    )
    object_id = models.PositiveIntegerField(default=0)
    condition = GenericForeignKey()
    negated = models.BooleanField(default=False)


class ArmamentCondition(models.Model):
    constraint = models.ForeignKey(Constraint, on_delete=models.CASCADE)
    slot = models.CharField(
        choices=ArmamentSlot.generate_choices(), max_length=ArmamentSlot.max_length()
    )
    weapon_groups = MultiSelectField(
        verbose_name=_('Weapon group'),
        choices=WeaponGroupEnum.generate_choices(),
        null=True,
        blank=True,
    )
    weapon_categories = MultiSelectField(
        verbose_name=_('Weapon category'),
        choices=WeaponCategoryIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    weapon_types = models.ManyToManyField(
        "base.WeaponType",
        verbose_name=_('Weapon type'),
        related_name='magic_weapons_conditions',
        blank=True,
        limit_choices_to={'is_enhanceable': True},
    )


class AvailabilityCondition(ClassAbstract):
    constraint = models.ForeignKey(
        Constraint, on_delete=models.CASCADE, related_name='availability_condition'
    )


class WeaponState(models.Model):
    is_empty = models.BooleanField(_('Is hand empty'), default=False)
    is_off_hand = models.BooleanField(default=False)
    category = MultiSelectField(
        verbose_name=_('Primary hand category'),
        choices=WeaponCategoryIntEnum.generate_choices(),
        null=True,
    )
    group = MultiSelectField(
        verbose_name=_('Primary hand group'),
        choices=WeaponGroupEnum.generate_choices(),
        null=True,
    )
    type = models.ManyToManyField(
        WeaponType,
        verbose_name=_('Primary hand'),
        blank=True,
        related_name='primary_hand_conditions',
    )


class ItemCondition(models.Model):
    constraint = models.ForeignKey(
        Constraint, on_delete=models.CASCADE, related_name='item_condition'
    )
    primary_hand = models.ForeignKey(
        WeaponState,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_hands',
    )
    secondary_hand = models.ForeignKey(
        WeaponState,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secondary_hands',
    )
    shield = MultiSelectField(
        verbose_name=_('Shield type'),
        choices=ShieldTypeIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    armor = MultiSelectField(
        verbose_name=_('Armor type'),
        choices=ArmorTypeIntEnum.generate_choices(),
        null=True,
        blank=True,
    )


class PropertiesCondition(models.Model):
    constraint = models.ForeignKey(
        Constraint, on_delete=models.CASCADE, related_name='scalar_conditions'
    )
    type = models.CharField(
        _('Property type'),
        choices=chain(
            AbilityEnum.generate_choices(is_sorted=False),
            NPCOtherProperties.generate_choices(
                condition=lambda x: x
                not in (NPCOtherProperties.ATTACK, NPCOtherProperties.DAMAGE)
            ),
            NPCClassProperties.generate_choices()
        ),
        max_length=max(
            map(
                lambda x: x.max_length(),
                (
                    AbilityEnum,
                    NPCOtherProperties,
                    NPCClassProperties,
                ),
            )
        ),
    )
    value = models.PositiveSmallIntegerField(
        verbose_name=_('Property value'), null=False
    )

    @property
    def value_display(self) -> str:
        if self.type == NPCClassProperties.POWER_SOURCE:
            return PowerSourceIntEnum(self.value).description
        return str(self.value)
