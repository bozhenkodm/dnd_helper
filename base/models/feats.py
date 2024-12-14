from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.abstract import ConstraintAbstract


class Feat(ConstraintAbstract):
    class Meta:
        verbose_name = _('Feat')
        verbose_name_plural = _('Feats')

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    min_level = models.PositiveSmallIntegerField(
        verbose_name=_('Minimal level'), default=1, choices=((1, 1), (11, 11), (21, 21))
    )
    text = models.TextField(verbose_name=_('Text'), null=True, blank=True)

    def __str__(self):
        return self.name
