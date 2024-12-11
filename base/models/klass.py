from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
    ArmorTypeIntEnum,
    ClassRoleEnum,
    NPCClassEnum,
    PowerSourceEnum,
    ShieldTypeIntEnum,
    WeaponCategoryIntEnum,
)
from base.managers import SubclassQuerySet
from base.models.skills import Skill


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
    )
    implement_types = models.ManyToManyField(
        'base.WeaponType',
        verbose_name=_('Available weapon types'),
        limit_choices_to={'primary_end__isnull': True},
        related_name='implement_%(app_label)s_%(class)s_wielders',
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


class Class(ClassAbstract):
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
    surges = models.PositiveSmallIntegerField(verbose_name=_('Surges'), default=6)
    hit_points_per_level = models.PositiveSmallIntegerField(
        verbose_name=_('Hit points per level'), default=5
    )
    hit_points_per_level_npc = models.PositiveSmallIntegerField(
        verbose_name=_('Hit points per level'), default=8
    )
    power_source = models.CharField(
        verbose_name=_('Power source'),
        choices=PowerSourceEnum.generate_choices(),
        max_length=PowerSourceEnum.max_length(),
    )
    role = models.CharField(
        verbose_name=_('Role'),
        choices=ClassRoleEnum.generate_choices(),
        max_length=ClassRoleEnum.max_length(),
    )
    mandatory_skills = models.ManyToManyField(Skill, verbose_name=_('Mandatory skills'))
    trainable_skills = models.ManyToManyField(
        Skill, verbose_name='Выборочно тренируемые навыки', related_name='classes'
    )

    def __str__(self):
        return self.name_display


class Subclass(ClassAbstract):
    class Meta:
        verbose_name = _('Subclass')
        verbose_name_plural = _('Subclasses')
        unique_together = ('klass', 'subclass_id')

    objects = SubclassQuerySet.as_manager()

    klass = models.ForeignKey(
        Class,
        verbose_name=_('Class'),
        on_delete=models.CASCADE,
        related_name='subclasses',
    )
    name = models.CharField(verbose_name=_('Name'), max_length=40)
    slug = models.CharField(verbose_name='Slug', max_length=40)
    subclass_id = models.PositiveSmallIntegerField(
        verbose_name=_('Subclass id'), default=0
    )

    def __str__(self):
        return f'{self.klass}, {self.name}'
