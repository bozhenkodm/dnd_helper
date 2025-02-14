from django.utils.translation import gettext_lazy as _

from base.models.magic_items import (
    ArmsSlotItem as BaseArmsSlotItem,
    MagicArmItemType as BaseMagicArmItemType,
    MagicArmorType as BaseMagicArmorType,
    MagicItemType as BaseMagicItemType,
    MagicWeaponType as BaseMagicWeaponType,
    SimpleMagicItem as BaseSimpleMagicItem,
)
from base.models.models import (
    Armor as BaseArmor,
    ArmorType as BaseArmorType,
    Weapon as BaseWeapon,
    WeaponType as BaseWeaponType,
)


class MagicItemType(BaseMagicItemType):
    class Meta:
        verbose_name = _('Magic item type')
        verbose_name_plural = _('Magic item types')
        proxy = True


class MagicArmItemType(BaseMagicArmItemType):
    class Meta:
        verbose_name = _('Magic shield/arms slot item type')
        verbose_name_plural = _('Magic shield/arms slot item types')
        proxy = True


class MagicArmorType(BaseMagicArmorType):
    class Meta:
        verbose_name = _('Magic armor type')
        verbose_name_plural = _('Magic armor types')
        proxy = True


class MagicWeaponType(BaseMagicWeaponType):
    class Meta:
        verbose_name = _('Magic weapon type')
        verbose_name_plural = _('Magic weapon types')
        proxy = True


class SimpleMagicItem(BaseSimpleMagicItem):
    class Meta:
        verbose_name = _('Magic item')
        verbose_name_plural = _('Magic items')
        proxy = True


class ArmsSlotItem(BaseArmsSlotItem):
    class Meta:
        verbose_name = _('Hand item/shield')
        verbose_name_plural = _('Hand items/shields')
        proxy = True


class Armor(BaseArmor):
    class Meta:
        verbose_name = _('Armor')
        verbose_name_plural = _('Armors')
        proxy = True


class ArmorType(BaseArmorType):
    class Meta:
        verbose_name = _('Armor type')
        verbose_name_plural = _('Armor types')
        proxy = True


class Weapon(BaseWeapon):
    class Meta:
        verbose_name = _('Weapon')
        verbose_name_plural = _('Weapons')
        proxy = True


class WeaponType(BaseWeaponType):
    class Meta:
        verbose_name = _('Weapon type')
        verbose_name_plural = _('Weapon types')
        proxy = True
