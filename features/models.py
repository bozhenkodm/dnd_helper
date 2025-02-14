from django.utils.translation import gettext_lazy as _

from base.models.feats import Feat as BaseFeat
from base.models.powers import Power as BasePower


class Power(BasePower):
    class Meta:
        verbose_name = _('Power')
        verbose_name_plural = _('Powers')
        proxy = True


class Feat(BaseFeat):
    class Meta:
        verbose_name = _('Feat')
        verbose_name_plural = _('Feats')
        proxy = True
