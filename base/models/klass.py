from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    ClassRoleIntEnum,
    NPCClassEnum,
    PowerSourceIntEnum,
)
from base.managers import SubclassQuerySet
from base.models.abstract import ClassAbstract
from base.models.items import BaseArmorType, ShieldType, WeaponCategory
from base.models.skills import Skill


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
    fortitude = models.PositiveSmallIntegerField(verbose_name=_('Fortitude'), default=0)
    reflex = models.PositiveSmallIntegerField(verbose_name=_('Reflex'), default=0)
    will = models.PositiveSmallIntegerField(verbose_name=_('Will'), default=0)
    surges = models.PositiveSmallIntegerField(verbose_name=_('Surges'), default=6)
    hit_points_per_level = models.PositiveSmallIntegerField(
        verbose_name=_('Hits per level'), default=5
    )
    hit_points_per_level_npc = models.PositiveSmallIntegerField(
        verbose_name=_('Hits per level'), default=8
    )
    power_source = models.PositiveSmallIntegerField(
        verbose_name=_('Power source'),
        choices=PowerSourceIntEnum.generate_choices(),
    )
    role = models.PositiveSmallIntegerField(
        verbose_name=_('Role'), choices=ClassRoleIntEnum.generate_choices()
    )
    mandatory_skills = models.ManyToManyField(
        Skill, verbose_name=_('Mandatory skills'), related_name='classes_for_mandatory'
    )
    trainable_skills = models.ManyToManyField(
        Skill, verbose_name=_('Selective trainable skills'), related_name='classes'
    )
    default_feats = models.ManyToManyField(
        'base.Feat', verbose_name=_('Default feats'), blank=True, related_name='classes'
    )
    default_powers = models.ManyToManyField(
        'base.Power',
        verbose_name=_('Default powers'),
        blank=True,
        related_name='classes',  # TODO rename related_name
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
    default_feats = models.ManyToManyField(
        'base.Feat',
        verbose_name=_('Default feats'),
        blank=True,
        related_name='subclasses',
    )
    default_powers = models.ManyToManyField(
        'base.Power',
        verbose_name=_('Default powers'),
        blank=True,
        related_name='subclasses',
    )

    def __str__(self):
        return f'{self.klass}, {self.name}'


class NPCClassAbstract(models.Model):
    class Meta:
        abstract = True

    klass = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name=_('Class'),
    )
    subclass_id = models.SmallIntegerField(
        verbose_name=_('Subclass'),
        default=0,
    )

    @property
    def subclass(self) -> Subclass:
        return self.klass.subclasses.get(subclass_id=self.subclass_id)

    @property
    def power_source(self) -> int:
        return self.klass.power_source

    @property
    def role(self) -> int:
        return self.klass.role

    @property
    def available_armor_types(self) -> models.QuerySet[BaseArmorType]:
        return BaseArmorType.objects.filter(
            models.Q(id__in=self.klass.armor_types.values_list('id', flat=True))
            | models.Q(id__in=self.subclass.armor_types.values_list('id', flat=True))
        )

    @property
    def available_shield_types(self) -> models.QuerySet[ShieldType]:
        return ShieldType.objects.filter(
            models.Q(id__in=self.klass.shields.values_list('id', flat=True))
            | models.Q(id__in=self.subclass.shields.values_list('id', flat=True))
        )

    @property
    def available_weapon_categories(self) -> models.QuerySet[WeaponCategory]:
        return WeaponCategory.objects.filter(
            models.Q(
                code__in=self.klass.weapon_categories.values_list('code', flat=True)
            )
            | models.Q(
                code__in=self.subclass.weapon_categories.values_list('code', flat=True)
            )
        )
