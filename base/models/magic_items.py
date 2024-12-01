from typing import ClassVar

from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
    ArmorTypeIntEnum,
    DiceIntEnum,
    MagicItemCategory,
    MagicItemSlot,
    ShieldTypeIntEnum,
)
from base.managers import ItemAbstractQuerySet
from base.objects import weapon_types_tuple


class MagicItemType(models.Model):
    class Meta:
        verbose_name = _('Magic item type')
        verbose_name_plural = _('Magic item types')

    name = models.CharField(verbose_name=_('Title'), max_length=100)
    min_level = models.PositiveSmallIntegerField(
        verbose_name=_('Minimal level'), default=1
    )
    max_level = models.PositiveSmallIntegerField(
        verbose_name=_('Maximum level'), default=30
    )
    step = models.PositiveSmallIntegerField(_('Level step'), default=5)
    category = models.CharField(
        verbose_name=_('Category'),
        choices=MagicItemCategory.generate_choices(is_sorted=False),
        default=MagicItemCategory.UNCOMMON,
        max_length=MagicItemCategory.max_length(),
    )
    picture = models.ImageField(
        verbose_name=_('Picture'), null=True, upload_to='items', blank=True
    )
    source = models.CharField(
        verbose_name=_('Source'),
        max_length=20,
        help_text=_('Book and page'),
        null=True,
        blank=True,
    )
    slot = models.CharField(
        verbose_name=_('Slot'),
        choices=MagicItemSlot.generate_choices(),
        max_length=MagicItemSlot.max_length(),
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    def level_range(self):
        return range(
            self.min_level,
            self.max_level + 1,
            self.step,
        )


class MagicArmorType(MagicItemType):
    class Meta:
        verbose_name = _('Magic armor type')
        verbose_name_plural = _('Magic armor types')

    armor_type_slots = MultiSelectField(
        verbose_name=_('Armor type slots'),
        choices=ArmorTypeIntEnum.generate_choices(),
        min_choices=1,
        null=False,
    )


class MagicArmItemType(MagicItemType):
    class Meta:
        verbose_name = _('Magic shield/arms slot item type')
        verbose_name_plural = _('Magic shield/arms slot item types')

    shield_slots = MultiSelectField(
        verbose_name=_('Shield slots'),
        choices=ShieldTypeIntEnum.generate_choices(
            condition=lambda x: x != ShieldTypeIntEnum.NONE
        ),
        null=True,
        blank=True,
    )


class MagicWeaponType(MagicItemType):
    class Meta:
        verbose_name = _('Magic weapon type')
        verbose_name_plural = _('Magic weapon types')

    weapon_type_slots = MultiSelectField(
        verbose_name=_('Weapon type'),
        choices=sorted(
            (w.slug(), w.name)
            for w in sorted(weapon_types_tuple, key=lambda x: x.name)
            if not w.is_magic_item and not w.primary_end
        ),
        null=False,
        min_choices=1,
    )
    crit_dice = models.SmallIntegerField(
        verbose_name=_('Crit dice'),
        choices=DiceIntEnum.generate_choices(condition=lambda x: x < DiceIntEnum.D20),
        null=True,
        blank=True,
        default=DiceIntEnum.D6,
    )
    crit_property = models.CharField(
        verbose_name=_('Crit property'),
        max_length=50,
        null=True,
        blank=True,
    )


class ItemAbstract(models.Model):
    class Meta:
        abstract = True

    objects = ItemAbstractQuerySet.as_manager()

    magic_item_type = models.ForeignKey(
        MagicItemType,
        verbose_name=_('Magic item type'),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    level = models.SmallIntegerField(verbose_name=_('Level'), default=0)

    @property
    def enhancement(self):
        if not self.magic_item_type:
            return 0
        return (self.level - 1) // 5 + 1

    @enhancement.setter
    def enhancement(self, value):
        pass

    @property
    def price(self):
        if not self.level:
            return 0
        return (200 + (self.level % 5) * 160) * (5 ** (self.level // 5))


class SimpleMagicItem(ItemAbstract):
    class Meta:
        verbose_name = _('Magic item')
        verbose_name_plural = _('Magic items')
        unique_together = ('magic_item_type', 'level')

    SLOT: ClassVar[MagicItemSlot]

    def __str__(self):
        return f'{self.magic_item_type} {self.level} уровня'


class NeckSlotItem(SimpleMagicItem):
    class Meta:
        proxy = True

    SLOT = MagicItemSlot.NECK

    @property
    def defence_bonus(self):
        return self.enhancement

    def __str__(self):
        return f'{self.magic_item_type}, +{self.enhancement}'


class HeadSlotItem(SimpleMagicItem):
    class Meta:
        proxy = True

    SLOT = MagicItemSlot.HEAD


class FeetSlotItem(SimpleMagicItem):
    class Meta:
        proxy = True

    SLOT = MagicItemSlot.FEET


class ArmsSlotItem(ItemAbstract):
    class Meta:
        verbose_name = _('Hand item/shield')
        verbose_name_plural = _('Hand items/shields')
        unique_together = ('magic_item_type', 'level', 'shield')

    SLOT = MagicItemSlot.ARMS

    shield = models.SmallIntegerField(
        verbose_name=_('Shield'),
        choices=ShieldTypeIntEnum.generate_choices(),
        default=ShieldTypeIntEnum.NONE,
    )

    def __str__(self):
        if self.magic_item_type and not self.shield:
            return f'{self.magic_item_type} {self.level} уровня'
        if not self.magic_item_type and self.shield:
            return self.get_shield_display()
        return (
            f'{self.magic_item_type} ({self.get_shield_display()}) {self.level} уровня'
        )


class WaistSlotItem(SimpleMagicItem):
    class Meta:
        proxy = True

    SLOT = MagicItemSlot.WAIST


class RingsSlotItem(SimpleMagicItem):
    class Meta:
        proxy = True

    SLOT = MagicItemSlot.RING


class HandsSlotItem(SimpleMagicItem):
    class Meta:
        proxy = True

    SLOT = MagicItemSlot.HANDS


class NPCMagicItemAbstract(models.Model):
    class Meta:
        abstract = True

    neck_slot = models.ForeignKey(
        NeckSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Neck slot'),
        related_name='npc_necks',
    )
    head_slot = models.ForeignKey(
        HeadSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Head slot'),
        related_name='npc_heads',
    )
    feet_slot = models.ForeignKey(
        FeetSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Feet slot'),
        related_name='npc_feet',
    )
    waist_slot = models.ForeignKey(
        WaistSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Waist slot'),
        related_name='npc_waists',
    )
    gloves_slot = models.ForeignKey(
        HandsSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Hands slot'),
        related_name='npc_arms',
    )
    left_ring_slot = models.ForeignKey(
        RingsSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Left hand ring'),
        related_name='npc_left_rings',
    )
    right_ring_slot = models.ForeignKey(
        RingsSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Right hand ring'),
        related_name='npc_right_rings',
    )
    arms_slot = models.ForeignKey(
        ArmsSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Arms slot'),
        related_name='npc_hands',
    )
