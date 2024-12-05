from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.base import generate_choices
from base.constants.constants import (
    AbilityEnum,
    BonusSource,
    BonusType,
    DefenceTypeEnum,
    PowerFrequencyEnum,
    SkillEnum,
)


class Bonus(models.Model):
    class Meta:
        verbose_name = _('Bonus')
        verbose_name_plural = _('Bonuses')

    name = models.CharField(
        verbose_name=_('Title'), max_length=100, null=True, blank=True
    )
    power = models.ForeignKey(
        "base.Power",
        verbose_name=_('Power'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='bonuses',
        related_query_name='bonus',
        limit_choices_to={'level': 0, 'frequency': PowerFrequencyEnum.PASSIVE},
    )
    race = models.ForeignKey(
        'base.Race',
        verbose_name=_('Race'),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='bonuses',
    )
    source = models.CharField(
        verbose_name=_('Bonus source'),
        choices=BonusSource.generate_choices(),
        max_length=BonusSource.max_length(),
        null=True,
        blank=True,
    )
    min_level = models.PositiveSmallIntegerField(
        default=1, verbose_name=_('Minimal level')
    )
    bonus_type = models.CharField(
        verbose_name=_('Bonus type'),
        choices=generate_choices(
            AbilityEnum, SkillEnum, DefenceTypeEnum, BonusType, is_sorted=False
        ),
        max_length=max(
            map(
                lambda x: x.max_length(),
                (
                    AbilityEnum,
                    SkillEnum,
                    DefenceTypeEnum,
                    BonusType,
                ),
            )
        ),
        null=True,
        blank=True,
    )
    value = models.CharField(
        verbose_name=_('Value'), null=True, blank=True, max_length=100
    )

    def __str__(self):
        return self.name or ''
