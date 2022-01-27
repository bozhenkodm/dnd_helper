from typing import ClassVar

from django.db import models
from multiselectfield import MultiSelectField  # type: ignore

from base.constants.constants import MagicItemCategory, MagicItemSlot


class MagicItemType(models.Model):
    class Meta:
        verbose_name = 'Тип магического предмета'
        verbose_name_plural = 'Типы магическогих предметов'

    name = models.CharField(verbose_name='Название', max_length=100)
    min_level = models.PositiveSmallIntegerField(
        verbose_name='Минимальный уровень', default=1
    )
    step = models.PositiveSmallIntegerField('Шаг повышения уровня', default=5)
    category = models.CharField(
        verbose_name='Категория',
        choices=MagicItemCategory.generate_choices(is_sorted=False),
        default=MagicItemCategory.UNCOMMON,
        max_length=MagicItemCategory.max_length(),
    )
    picture = models.ImageField(
        verbose_name='Картинка', null=True, upload_to='items', blank=True
    )
    source = models.CharField(
        verbose_name='Источник',
        max_length=20,
        help_text='Книга и страница',
        null=True,
        blank=True,
    )
    slots = MultiSelectField(
        verbose_name='Слоты',
        choices=MagicItemSlot.generate_choices(),
        min_choices=1,
        null=True,
    )

    def __str__(self):
        return self.name


class ItemAbstract(models.Model):
    class Meta:
        abstract = True

    magic_item_type = models.ForeignKey(
        MagicItemType,
        verbose_name='Магический предмет',
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    level = models.SmallIntegerField(verbose_name='Уровень', default=0)

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
        verbose_name_plural = 'Магические предметы'

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


class NPCMagicItemAbstract(models.Model):
    class Meta:
        abstract = True

    neck_slot = models.ForeignKey(
        NeckSlotItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Предмет на шею',
    )


# HEAD = 'head', ''
# ARMS = 'arms', ''
# FEET = 'feet', ''
# HANDS = 'hands', ''
# WAIST = 'waist', ''
# RINGS = 'rings', ''
# WONDROUS_ITEMS = 'wondrous_items', ''
# TATOO = 'tatoo', ''
