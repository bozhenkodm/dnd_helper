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
    """Represents a D&D character class (e.g., Fighter, Wizard, Rogue).

    Contains class-specific attributes like saving throw bonuses, hit points,
    power source, role, and available skills/feats/powers.
    """

    class Meta:
        verbose_name = _('Class')
        verbose_name_plural = _('Classes')
        ordering = ('name_display',)

    # Class identification
    name = models.SlugField(
        choices=NPCClassEnum.generate_choices(is_sorted=False),
        max_length=NPCClassEnum.max_length(),
    )
    name_display = models.CharField(
        verbose_name=_('Title'),
        max_length=NPCClassEnum.max_description_length(),
    )

    # Defences bonuses
    fortitude = models.PositiveSmallIntegerField(verbose_name=_('Fortitude'), default=0)
    reflex = models.PositiveSmallIntegerField(verbose_name=_('Reflex'), default=0)
    will = models.PositiveSmallIntegerField(verbose_name=_('Will'), default=0)

    # Health and healing surges
    surges = models.PositiveSmallIntegerField(verbose_name=_('Surges'), default=6)
    hit_points_per_level = models.PositiveSmallIntegerField(
        verbose_name=_('Hits per level'), default=5
    )
    # NPCs typically have more hit points than player characters
    hit_points_per_level_npc = models.PositiveSmallIntegerField(
        verbose_name=_('Hits per level'), default=8
    )

    # Class categorization
    power_source = models.PositiveSmallIntegerField(
        verbose_name=_('Power source'),
        choices=PowerSourceIntEnum.generate_choices(),
    )
    role = models.PositiveSmallIntegerField(
        verbose_name=_('Role'), choices=ClassRoleIntEnum.generate_choices()
    )
    # Skills that all characters of this class must have
    mandatory_skills = models.ManyToManyField(
        Skill, verbose_name=_('Mandatory skills'), related_name='classes_for_mandatory'
    )
    # Skills that characters of this class can choose to train in
    trainable_skills = models.ManyToManyField(
        Skill, verbose_name=_('Selective trainable skills'), related_name='classes'
    )
    # Feats automatically granted to all characters of this class
    default_feats = models.ManyToManyField(
        'base.Feat', verbose_name=_('Default feats'), blank=True, related_name='classes'
    )
    # Powers automatically granted to all characters of this class
    default_powers = models.ManyToManyField(
        'base.Power',
        verbose_name=_('Default powers'),
        blank=True,
        related_name='classes',  # TODO rename related_name
    )

    def __str__(self):
        return self.name_display


class Subclass(ClassAbstract):
    """Represents a specialization within a class (e.g., Fighter's Guardian or Great Weapon Fighter).

    Subclasses provide additional customization and specialization options
    while maintaining the base class structure.
    """

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
    # Numeric identifier for the subclass within its parent class
    subclass_id = models.PositiveSmallIntegerField(
        verbose_name=_('Subclass id'), default=0
    )
    # Additional feats granted by this subclass specialization
    default_feats = models.ManyToManyField(
        'base.Feat',
        verbose_name=_('Default feats'),
        blank=True,
        related_name='subclasses',
    )
    # Additional powers granted by this subclass specialization
    default_powers = models.ManyToManyField(
        'base.Power',
        verbose_name=_('Default powers'),
        blank=True,
        related_name='subclasses',
    )

    def __str__(self):
        return f'{self.klass}, {self.name}'


class NPCClassAbstract(models.Model):
    """Abstract base class for NPCs that have a class and subclass.

    Provides common functionality for accessing class-related properties
    and available equipment types based on class and subclass restrictions.
    """

    class Meta:
        abstract = True

    klass = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name=_('Class'),
    )
    # ID of the subclass within the parent class
    subclass_id = models.SmallIntegerField(
        verbose_name=_('Subclass'),
        default=0,
    )

    @property
    def subclass(self) -> Subclass:
        """Get the specific subclass instance for this NPC."""
        return self.klass.subclasses.get(subclass_id=self.subclass_id)

    @property
    def power_source(self) -> int:
        """Get the power source from the NPC's class."""
        return self.klass.power_source

    @property
    def role(self) -> int:
        """Get the role from the NPC's class."""
        return self.klass.role

    @property
    def available_armor_types(self) -> models.QuerySet[BaseArmorType]:
        """Get all armor types available to this NPC's class and subclass."""
        return BaseArmorType.objects.filter(
            models.Q(id__in=self.klass.armor_types.values_list('id', flat=True))
            | models.Q(id__in=self.subclass.armor_types.values_list('id', flat=True))
        )

    @property
    def available_shield_types(self) -> models.QuerySet[ShieldType]:
        """Get all shield types available to this NPC's class and subclass."""
        return ShieldType.objects.filter(
            models.Q(id__in=self.klass.shields.values_list('id', flat=True))
            | models.Q(id__in=self.subclass.shields.values_list('id', flat=True))
        )

    @property
    def available_weapon_categories(self) -> models.QuerySet[WeaponCategory]:
        """Get all weapon categories available to this NPC's class and subclass."""
        return WeaponCategory.objects.filter(
            models.Q(
                code__in=self.klass.weapon_categories.values_list('code', flat=True)
            )
            | models.Q(
                code__in=self.subclass.weapon_categories.values_list('code', flat=True)
            )
        )
