from itertools import chain

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
    AbilityEnum,
    ArmamentSlot,
    NPCOtherProperties,
    WeaponCategoryIntEnum,
    WeaponGroupEnum,
)
from base.models.abstract import ClassAbstract


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
    condition = GenericForeignKey("content_type", "object_id")
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
    constraint = models.ForeignKey(Constraint, on_delete=models.CASCADE)


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
        ),
        max_length=max(
            map(
                lambda x: x.max_length(),
                (
                    AbilityEnum,
                    NPCOtherProperties,
                ),
            )
        ),
    )
    value = models.PositiveSmallIntegerField(
        verbose_name=_('Property value'), null=False
    )
