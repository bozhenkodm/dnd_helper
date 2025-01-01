import operator
import typing
from itertools import chain

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    MODEL_NAME_TO_NPC_FIELD,
    AbilityEnum,
    ClassRoleIntEnum,
    NPCOtherProperties,
    PowerSourceIntEnum,
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
                'skill',
            ),
        },
    )
    object_id = models.PositiveIntegerField(default=0)
    condition = GenericForeignKey()
    negated = models.BooleanField(default=False)

    def _field_fits(self, npc, field_name) -> bool:
        field = getattr(npc, field_name)
        if isinstance(field, models.Manager):  # checking if it is a many to many
            return (self.condition in field.all()) != self.negated
        return (field == self.condition) != self.negated

    def fits(self, npc) -> bool:
        field_name = MODEL_NAME_TO_NPC_FIELD.get(
            self.content_type.model,
            self.content_type.model,
        )
        return self._field_fits(npc, field_name)


class AvailabilityCondition(ClassAbstract):
    constraint = models.ForeignKey(
        Constraint, on_delete=models.CASCADE, related_name='availability_conditions'
    )

    def fits(self, npc) -> bool:
        if self.armor_types and not set(npc.available_armor_types) & set(
            map(int, self.armor_types)
        ):
            return False
        if self.shields and not set(npc.available_shield_types) & set(
            map(int, self.shields)
        ):
            return False
        if self.weapon_categories and not set(npc.available_weapon_categories) & set(
            map(int, self.weapon_categories)
        ):
            return False
        if self.weapon_types.all() and not (
            set(npc.klass.weapon_types.values_list('category', flat=True).distinct())
            & set(self.weapon_categories)
            or npc.klass.weapon_types.intersection(self.weapon_types.all()).count()
        ):
            return False
        if self.implement_types.all() and not (
            npc.klass.implement_types.intersection(self.implement_types.all()).count()
        ):
            return False

        return True


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

    def __str__(self):
        return f'{self.type.lower()}: {self.value}'

    @property
    def value_display(self) -> str:
        if self.type == NPCOtherProperties.POWER_SOURCE:
            return PowerSourceIntEnum(self.value).description
        if self.type == NPCOtherProperties.ROLE:
            return ClassRoleIntEnum(self.value).description
        return str(self.value)

    @property
    def op(self) -> typing.Callable:
        if self.type in (NPCOtherProperties.POWER_SOURCE, NPCOtherProperties.ROLE):
            return operator.eq
        return operator.ge

    def fits(self, npc) -> bool:
        return self.op(getattr(npc, self.type.lower()), self.value)
