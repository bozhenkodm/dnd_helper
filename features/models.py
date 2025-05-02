from django.utils.translation import gettext_lazy as _

from base.models.feats import Feat as BaseFeat
from base.models.powers import Power as BasePower


class Power(BasePower):
    class Meta:
        verbose_name = _('Power')
        verbose_name_plural = _('Powers')
        proxy = True


class ClassPower(BasePower):
    class Meta:
        verbose_name = _('Class power')
        verbose_name_plural = _('Class powers')
        proxy = True


class SubclassPower(BasePower):
    class Meta:
        verbose_name = _('Subclass power')
        verbose_name_plural = _('Subclass powers')
        proxy = True


class RacePower(BasePower):
    class Meta:
        verbose_name = _('Race power')
        verbose_name_plural = _('Race powers')
        proxy = True


class FunctionalTemplatePower(BasePower):
    class Meta:
        verbose_name = _('Functional template power')
        verbose_name_plural = _('Functional template powers')
        proxy = True


class ParagonPathPower(BasePower):
    class Meta:
        verbose_name = _('Paragon path power')
        verbose_name_plural = _('Paragon path powers')
        proxy = True


class MagicItemTypePower(BasePower):
    class Meta:
        verbose_name = _('Magic item type power')
        verbose_name_plural = _('Magic item type powers')
        proxy = True


class SkillPower(BasePower):
    class Meta:
        verbose_name = _('Skill power')
        verbose_name_plural = _('Skill powers')
        proxy = True


class Feat(BaseFeat):
    class Meta:
        verbose_name = _('Feat')
        verbose_name_plural = _('Feats')
        proxy = True
