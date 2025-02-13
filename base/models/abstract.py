from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
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

    @classmethod
    def get_ids_for_npc(cls, npc, initial_query=None):
        ids = set()
        if initial_query:
            queryset = cls.objects.filter(initial_query)
        else:
            queryset = cls.objects.all()
        for item in queryset:
            constraints_queryset = item.constraints.all()
            if not constraints_queryset:
                ids.add(item.id)
                continue
            for constraint in constraints_queryset:
                fits = True
                for condition in constraint.conditions.all():
                    if not condition.fits(npc):
                        fits = False
                        break
                for condition in constraint.scalar_conditions.all():
                    if not condition.fits(npc):
                        fits = False
                        break
                for condition in constraint.availability_conditions.all():
                    if not condition.fits(npc):
                        fits = False
                        break
                if fits:
                    ids.add(item.id)
                    break
        return ids
