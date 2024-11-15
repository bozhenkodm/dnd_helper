from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import BonusSource, BonusType


class Bonus(models.Model):
    class Meta:
        verbose_name = _('Bonus')
        verbose_name_plural = _('Bonuses')

    name = models.CharField(
        verbose_name=_('Title'), max_length=100, null=True, blank=True
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
        choices=BonusType.generate_choices(),
        max_length=BonusType.max_length(),
        null=True,
        blank=True,
    )
    value = models.CharField(
        verbose_name=_('Value'), null=True, blank=True, max_length=100
    )

    def __str__(self):
        return self.name
