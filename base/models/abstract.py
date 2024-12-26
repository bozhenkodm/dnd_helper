from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
    MODEL_NAME_TO_NPC_FIELD,
    ArmorTypeIntEnum,
    ShieldTypeIntEnum,
    WeaponCategoryIntEnum,
)


class ClassAbstract(models.Model):
    class Meta:
        abstract = True

    weapon_categories = MultiSelectField(
        verbose_name=_('Available weapon categories'),
        choices=WeaponCategoryIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    weapon_types = models.ManyToManyField(
        'base.WeaponType',
        verbose_name=_('Available weapon types'),
        limit_choices_to={'primary_end__isnull': True},
        related_name='weapon_%(app_label)s_%(class)s_wielders',
        blank=True,
    )
    implement_types = models.ManyToManyField(
        'base.WeaponType',
        verbose_name=_('Available implement types'),
        limit_choices_to={'primary_end__isnull': True},
        related_name='implement_%(app_label)s_%(class)s_wielders',
        blank=True,
    )
    armor_types = MultiSelectField(
        verbose_name=_('Available armor types'),
        choices=ArmorTypeIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    shields = MultiSelectField(
        verbose_name=_('Available shields'),
        choices=ShieldTypeIntEnum.generate_choices(
            lambda x: x != ShieldTypeIntEnum.NONE
        ),
        null=True,
        blank=True,
    )


class ConstraintAbstract(models.Model):
    class Meta:
        abstract = True

    constraints = GenericRelation("base.Constraint")

    @staticmethod
    def _field_fits(npc, field_name, condition) -> bool:
        field = getattr(npc, field_name)
        if isinstance(field, models.Manager):  # checking if it is a many to many
            return (condition.condition in field.all()) != condition.negated
        return (field == condition.condition) != condition.negated

    @classmethod
    def get_ids_for_npc(cls, npc, initial_query=None):
        ids = set()
        if initial_query:
            queryset = cls.objects.filter(initial_query)
        else:
            queryset = cls.objects.all()
        for item in queryset:
            if not item.constraints.count():
                ids.add(item.id)
                continue
            for constraint in item.constraints.all():
                is_fit = True
                for condition in constraint.conditions.all():
                    field_name = MODEL_NAME_TO_NPC_FIELD.get(
                        condition.content_type.model,
                        condition.content_type.model,
                    )
                    if not cls._field_fits(npc, field_name, condition):
                        is_fit = False
                        break
                for condition in constraint.scalar_conditions.all():
                    if getattr(npc, condition.type.lower()) < condition.value:
                        is_fit = False
                        break
                for condition in constraint.availability_conditions.all():
                    if not condition.fits(npc):
                        is_fit = False
                        break
                if is_fit:
                    ids.add(item.id)
                    break
        return ids
