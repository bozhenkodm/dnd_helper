from typing import ClassVar

from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
    ArmorTypeIntEnum,
    MagicItemCategory,
    MagicItemSlot,
    ShieldTypeIntEnum,
)


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
    slots = MultiSelectField(
        verbose_name=_('Slots'),
        choices=MagicItemSlot.generate_choices(),
        min_choices=1,
        null=True,
    )
    # properties = models.JSONField(null=True)

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

    # def clean(self):
    #     if MagicItemSlot.ARMOR not in self.slots:
    #         raise ValidationError(_("Magic armor type object must have armor slot."))
    #     super().clean()


class ItemAbstract(models.Model):
    class Meta:
        abstract = True

    magic_item_type = models.ForeignKey(
        MagicItemType,
        verbose_name=_('Magic item type'),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    level = models.SmallIntegerField(verbose_name=_('Level'), default=0)

    @property
    def enchantment(self):
        if not self.magic_item_type:
            return 0
        return (self.level - 1) // 5 + 1

    @property
    def price(self):
        if not self.level:
            return 0
        return (200 + (self.level % 5) * 160) * (5 ** (self.level // 5))


class SimpleMagicItem(ItemAbstract):
    class Meta:
        verbose_name = 'Магический предмет'
        # verbose_name = _('Magic item')
        verbose_name_plural = 'Магические предметы'
        # verbose_name_plural = _('Magic items')
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
        return self.enchantment


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
        # verbose_name = _('Hand item/shield')
        # verbose_name_plural = _('Hand items/shields')
        verbose_name = 'Предмет на руки/щит'
        verbose_name_plural = 'Предметы на руки/щиты'
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
