from functools import cached_property
from typing import ClassVar

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    ArmorTypeIntEnum,
    DiceIntEnum,
    MagicItemCategory,
    MagicItemSlot,
    PowerActionTypeEnum,
    ShieldTypeIntEnum,
    ThrownWeaponType,
    WeaponCategoryIntEnum,
    WeaponGroupEnum,
    WeaponHandednessEnum,
)
from base.exceptions import WrongWeapon
from base.managers import ItemAbstractQuerySet
from base.models.books import BookSource
from base.objects.dice import DiceRoll


class BaseArmorType(models.Model):
    """Base armor type with fundamental armor statistics."""

    armor_class = models.PositiveSmallIntegerField(
        verbose_name=_('Name'), choices=ArmorTypeIntEnum.generate_choices(), unique=True
    )
    is_light = models.BooleanField(verbose_name=_('Is light?'), default=True)
    speed_penalty = models.SmallIntegerField(verbose_name=_('Speed penalty'), default=0)
    skill_penalty = models.SmallIntegerField(
        verbose_name=_('Skills penalty'), default=0
    )

    def __str__(self) -> str:
        return self.get_armor_class_display()


class ArmorType(models.Model):
    """Specific armor type extending base armor with additional properties."""

    class Meta:
        verbose_name = _('Armor type')
        verbose_name_plural = _('Armor types')

    name = models.CharField(verbose_name=_('Title'), max_length=100)
    base_armor_type = models.ForeignKey(
        BaseArmorType,
        verbose_name=_('Armor type'),
        on_delete=models.CASCADE,
    )
    bonus_armor_class = models.PositiveSmallIntegerField(
        verbose_name=_('Additional armor class'),
        default=0,
    )
    speed_penalty = models.SmallIntegerField(verbose_name=_('Speed penalty'), default=0)
    skill_penalty = models.SmallIntegerField(
        verbose_name=_('Skills penalty'), default=0
    )
    minimal_enhancement = models.PositiveSmallIntegerField(
        verbose_name=_('Minimal enhancement'), default=0
    )
    fortitude_bonus = models.PositiveSmallIntegerField(
        verbose_name=_('Fortitude bonus'), default=0
    )
    reflex_bonus = models.PositiveSmallIntegerField(
        verbose_name=_('Reflex bonus'), default=0
    )
    will_bonus = models.PositiveSmallIntegerField(
        verbose_name=_('Will bonus'), default=0
    )
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f'{self.base_armor_type}, ({self.name})'

    @property
    def armor_class(self) -> int:
        """Calculate total armor class including base and bonus."""
        return self.base_armor_type.armor_class + self.bonus_armor_class

    @property
    def is_light(self) -> bool:
        """Check if armor is light type based on base armor type."""
        return self.base_armor_type.is_light


class ShieldType(models.Model):
    """Shield type with defensive properties."""

    class Meta:
        verbose_name = _('Shield type')
        verbose_name_plural = _('Shield types')

    base_shield_type = models.PositiveSmallIntegerField(
        verbose_name=_('Armor type'),
        choices=ShieldTypeIntEnum.generate_choices(),
    )
    skill_penalty = models.SmallIntegerField(
        verbose_name=_('Skills penalty'), default=0
    )

    def __str__(self) -> str:
        return self.get_base_shield_type_display()


class WeaponHandedness(models.Model):
    """Weapon handedness properties (one-handed, two-handed, off-hand)."""

    name = models.CharField(
        verbose_name=_('Handedness'),
        choices=WeaponHandednessEnum.generate_choices(is_sorted=False),
        max_length=WeaponHandednessEnum.max_length(),
        unique=True,
    )
    is_one_handed = models.BooleanField(
        verbose_name=_('One handed'), default=True, null=True
    )

    def __str__(self) -> str:
        return self.get_name_display()

    @property
    def is_no_hand(self) -> bool:
        """Check if weapon requires no hands (ki focus or holy symbol)."""
        return self.is_one_handed is None

    @property
    def is_off_hand(self) -> bool:
        """Check if weapon is used in off-hand."""
        return self.name == WeaponHandednessEnum.OFF_HAND

    @property
    def is_two_handed(self) -> bool:
        """Check if weapon requires two hands."""
        return self.is_one_handed is False


class WeaponGroup(models.Model):
    """Weapon group classification (e.g., sword, bow, axe)."""

    class Meta:
        verbose_name = _('Weapon group')
        verbose_name_plural = _('Weapon group')
        ordering = ('is_ranged', WeaponGroupEnum.generate_case())

    name = models.CharField(
        verbose_name=_('Name'),
        choices=WeaponGroupEnum.generate_choices(),
        max_length=WeaponGroupEnum.max_length(),
        unique=True,
    )
    is_ranged = models.BooleanField(verbose_name=_('Ranged'), default=False)

    def __str__(self):
        return self.get_name_display()


class WeaponCategory(models.Model):
    """Weapon category classification (simple, martial, superior)."""

    class Meta:
        verbose_name = _('Weapon category')
        verbose_name_plural = _('Weapon categories')

    code = models.PositiveSmallIntegerField(
        verbose_name=_('Category'),
        choices=WeaponCategoryIntEnum.generate_choices(),
        unique=True,
    )
    is_ranged = models.BooleanField(verbose_name=_('Ranged'), null=True)
    category = models.PositiveSmallIntegerField(
        verbose_name=_('Base category'),
        choices=WeaponCategoryIntEnum.generate_choices(
            condition=lambda x: x <= WeaponCategoryIntEnum.SUPERIOR
        ),
        null=True,
    )

    def __str__(self):
        return self.get_code_display()


class WeaponType(models.Model):
    """Specific weapon type with all combat statistics and properties."""

    class Meta:
        verbose_name = _('Weapon type')
        verbose_name_plural = _('Weapon types')

    name = models.CharField(verbose_name=_('Title'), max_length=30, blank=True)
    slug = models.CharField(verbose_name='Slug', max_length=30, unique=True, blank=True)
    handedness = models.ForeignKey(
        WeaponHandedness,
        verbose_name=_('Handedness'),
        on_delete=models.CASCADE,
        null=True,
    )
    groups = models.ManyToManyField(WeaponGroup, verbose_name=_('Groups'), blank=False)
    category = models.ForeignKey(
        WeaponCategory, verbose_name=_('Category'), on_delete=models.CASCADE
    )
    range = models.PositiveSmallIntegerField(
        verbose_name=_('Range'), default=0, help_text=_('For ranged weapon')
    )
    distance = models.PositiveSmallIntegerField(
        verbose_name=_('Distance'),
        default=1,
        help_text=_('Melee distance'),
    )
    prof_bonus = models.PositiveSmallIntegerField(
        verbose_name=_('Prof bonus'), default=2
    )
    dice = models.PositiveSmallIntegerField(
        choices=DiceIntEnum.generate_choices(lambda x: x <= DiceIntEnum.D12), null=True
    )
    dice_number = models.PositiveSmallIntegerField(default=1)

    brutal = models.PositiveSmallIntegerField(default=0)
    thrown = models.CharField(
        choices=ThrownWeaponType.generate_choices(),
        max_length=ThrownWeaponType.max_length(),
        null=True,
    )
    is_high_crit = models.BooleanField(default=False)
    load = models.CharField(
        choices=(
            (
                PowerActionTypeEnum.FREE.value,
                f'Зарядка: {PowerActionTypeEnum.FREE.description}',
            ),
            (
                PowerActionTypeEnum.MINOR.value,
                f'Зарядка: {PowerActionTypeEnum.MINOR.description}',
            ),
        ),
        max_length=5,
        null=True,
    )
    is_small = models.BooleanField(default=False)
    is_defensive = models.BooleanField(default=False)
    primary_end = models.OneToOneField(
        'self',
        verbose_name=_('Primary end'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='secondary_end',
    )
    is_enhanceable = models.BooleanField(
        verbose_name=_('Is weapon enhanceable?'), default=True
    )
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    @property
    def max_range(self):
        """Calculate maximum range for ranged weapons (double normal range)."""
        return self.range * 2

    @property
    def is_ranged(self) -> bool:
        """Check if weapon is ranged based on range value."""
        return self.range > 0

    @property
    def is_reach(self) -> bool:
        """Check if weapon has reach property (distance of 2)."""
        return self.distance == 2

    def damage(self, weapon_number=1) -> str:
        """Get damage string representation for weapon(s)."""
        return f'{self.dice_number * weapon_number}{self.get_dice_display()}'

    @property
    def is_melee(self) -> bool:
        """Check if weapon can be used in melee based on distance."""
        return bool(self.distance)

    @property
    def is_double(self) -> bool:
        """Check if weapon is double-ended (has primary and secondary ends)."""
        try:
            return bool(self.primary_end or self.secondary_end)
        except WeaponType.DoesNotExist:
            return False

    @property
    def properties_text(self) -> str:
        """Generate comma-separated text of weapon properties."""
        # TODO localization
        result = []
        if self.brutal:
            result.append(f'Жестокое {self.brutal}')
        if self.thrown:
            result.append(self.get_thrown_display())
        if self.is_high_crit:
            result.append('Высококритичное')
        if self.is_reach:
            result.append('Досягаемость')
        if self.load:
            result.append(self.get_load_display())
        if self.is_small:
            result.append('Маленькое')
        if self.is_defensive:
            result.append('Защитное')
        return ', '.join(result)


class MagicItemType(models.Model):
    """Base magic item type with level scaling and categorization."""

    class Meta:
        verbose_name = _('Magic item type')
        verbose_name_plural = _('Magic item types')
        ordering = ('name',)

    name = models.CharField(verbose_name=_('Title'), max_length=100)
    min_level = models.PositiveSmallIntegerField(
        verbose_name=_('Minimal level'), default=1
    )
    max_level = models.PositiveSmallIntegerField(
        verbose_name=_('Maximum level'), default=30
    )
    step = models.PositiveSmallIntegerField(
        _('Level step'), default=5, choices=((5, 5), (10, 10))
    )
    category = models.CharField(
        verbose_name=_('Category'),
        choices=MagicItemCategory.generate_choices(is_sorted=False),
        default=MagicItemCategory.UNCOMMON.value,
        max_length=MagicItemCategory.max_length(),
    )
    picture = models.ImageField(
        verbose_name=_('Picture'), null=True, upload_to='items', blank=True
    )
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
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
        """Generate range of valid levels for this magic item type."""
        return range(
            self.min_level,
            self.max_level + 1,
            self.step,
        )


class MagicArmorType(MagicItemType):
    """Magic item type specifically for armor with compatible armor types."""

    class Meta:
        verbose_name = _('Magic armor type')
        verbose_name_plural = _('Magic armor types')

    armor_type_slots = models.ManyToManyField(
        BaseArmorType,
        verbose_name=_('Armor type slots'),
    )


class MagicArmItemType(MagicItemType):
    """Magic item type for arms/shield slot items."""

    class Meta:
        verbose_name = _('Magic shield/arms slot item type')
        verbose_name_plural = _('Magic shield/arms slot item types')

    shield_slots = models.ManyToManyField(
        ShieldType, verbose_name=_('Shield slots'), blank=True
    )


class MagicWeaponType(MagicItemType):
    """Magic item type for weapons with weapon restrictions and crit properties."""

    class Meta:
        verbose_name = _('Magic weapon type')
        verbose_name_plural = _('Magic weapon types')

    weapon_groups = models.ManyToManyField(
        WeaponGroup, verbose_name=_('Weapon group'), blank=True
    )
    weapon_categories = models.ManyToManyField(
        WeaponCategory, verbose_name=_('Weapon category'), blank=True
    )
    weapon_types = models.ManyToManyField(
        WeaponType,
        verbose_name=_('Weapon type'),
        related_name='magic_weapons',
        blank=True,
        limit_choices_to={'is_enhanceable': True},
    )
    implement_type = models.ForeignKey(
        WeaponType,
        verbose_name=_('Implement type'),
        help_text=_('Does item has additional implement property?'),
        null=True,
        blank=True,
        limit_choices_to={'category__code': WeaponCategoryIntEnum.IMPLEMENT.value},
        on_delete=models.SET_NULL,
    )
    crit_dice = models.SmallIntegerField(
        verbose_name=_('Crit dice'),
        choices=DiceIntEnum.generate_choices(condition=lambda x: x < DiceIntEnum.D20),
        null=True,
        blank=True,
        default=DiceIntEnum.D6.value,
    )
    crit_property = models.CharField(
        verbose_name=_('Crit property'),
        max_length=50,
        null=True,
        blank=True,
    )


class ItemAbstract(models.Model):
    """Abstract base class for all items with magic properties and level scaling."""

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
        """Calculate enhancement bonus based on item level (every 5 levels)."""
        if not self.magic_item_type:
            return 0
        return (self.level - 1) // 5 + 1

    @enhancement.setter
    def enhancement(self, value):
        pass

    @property
    def price(self):
        """Calculate item price based on level using D&D 4e pricing formula."""
        if not self.level:
            return 0
        return (200 + (self.level % 5) * 160) * (5 ** (self.level // 5))


class Armor(ItemAbstract):
    """Armor item with armor type and enhancement bonuses."""

    class Meta:
        verbose_name = _('Armor')
        verbose_name_plural = _('Armors')

    armor_type = models.ForeignKey(
        ArmorType,
        verbose_name=_('Armor type'),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'{self.name}, +{self.enhancement}'

    @property
    def armor_class(self) -> int:
        """Calculate total armor class including base AC and enhancement."""
        return self.armor_type.armor_class + self.enhancement

    @property
    def speed_penalty(self):
        """Get speed penalty from armor type."""
        return self.armor_type.speed_penalty

    @property
    def skill_penalty(self):
        """Get skill penalty from armor type."""
        return self.armor_type.skill_penalty

    @property
    def name(self) -> str:
        """Generate full armor name including magic item type if present."""
        magic_item_type = (
            f', {self.magic_item_type.name}' if self.magic_item_type else ''
        )
        return f'{self.armor_type}{magic_item_type}'

    @property
    def is_light(self) -> bool:
        """Check if armor is light type."""
        return self.armor_type.is_light

    @classmethod
    def create_on_base(
        cls, armor_type: ArmorType, magic_armor_type: MagicArmorType, level: int
    ):
        """Create magic armor if it meets enhancement requirements and doesn't exist."""
        if (level - 1) // 5 + 1 < armor_type.minimal_enhancement:
            return
        if not cls.objects.filter(
            magic_item_type=magic_armor_type, armor_type=armor_type, level=level
        ).exists():
            magic_item = cls(
                magic_item_type=magic_armor_type, armor_type=armor_type, level=level
            )
            magic_item.save()


class Weapon(ItemAbstract):
    """Weapon item with weapon type and enhancement bonuses."""

    class Meta:
        verbose_name = _('Weapon')
        verbose_name_plural = _('Weapons')
        unique_together = ('magic_item_type', 'level', 'weapon_type')

    weapon_type = models.ForeignKey(
        WeaponType,
        verbose_name=_('Weapon type'),
        on_delete=models.CASCADE,
        related_name='weapons',
    )

    def __str__(self):
        return f'{self.title}, +{self.enhancement}'

    @property
    def title(self) -> str:
        """Generate weapon title including magic item type if present."""
        if not self.magic_item_type:
            return str(self.weapon_type)
        return f'{self.weapon_type}, {self.magic_item_type}'

    @property
    def damage(self):
        """Get damage string representation including enhancement bonus."""
        if not self.enhancement:
            return (
                f'{self.weapon_type.dice_number}{self.weapon_type.get_dice_display()}'
            )
        return (
            f'{self.weapon_type.dice_number}'
            f'{self.weapon_type.get_dice_display()}'
            f'{self.enhancement}'
        )

    @property
    def damage_roll(self) -> DiceRoll:
        """Get DiceRoll object for damage calculation."""
        return DiceRoll(
            rolls=self.weapon_type.dice_number,
            dice=DiceIntEnum(self.weapon_type.dice),
            addendant=self.enhancement,
        )

    @property
    def prof_bonus(self):
        """Get proficiency bonus from weapon type."""
        return self.weapon_type.prof_bonus

    @cached_property
    def handedness(self):
        """Get weapon handedness with caching."""
        return self.weapon_type.handedness

    def groups(self):
        """Get all weapon groups this weapon belongs to."""
        return self.weapon_type.groups.all()

    @cached_property
    def category(self):
        """Get weapon category with caching."""
        return self.weapon_type.category

    @property
    def is_double(self) -> bool:
        """Check if weapon is double-ended."""
        return self.weapon_type.is_double

    def get_attack_type(self, is_melee: bool, is_ranged: bool) -> str:
        """Generate attack type string based on melee/ranged capabilities."""
        # TODO localization
        melee_attack_type, ranged_attack_type = '', ''
        is_melee = is_melee and self.weapon_type.is_melee
        is_ranged = is_ranged and self.weapon_type.is_ranged
        if is_melee:
            melee_attack_type = f'Рукопашный {self.weapon_type.distance}'
        if is_ranged:
            ranged_attack_type = (
                f'Дальнобойный {self.weapon_type.range}/{self.weapon_type.max_range}'
            )
        if is_melee and is_ranged:
            return f'{melee_attack_type} или {ranged_attack_type}'
        if is_melee:
            return melee_attack_type
        if is_ranged:
            return ranged_attack_type
        raise WrongWeapon(
            f'Wrong attack type: {self}, melee: {is_melee}, ranged: {is_ranged}'
        )

    @classmethod
    def create_on_base(
        cls, weapon_type: WeaponType, magic_weapon_type: MagicWeaponType, level: int
    ):
        """Create magic weapon if it doesn't already exist."""
        if not cls.objects.filter(
            magic_item_type=magic_weapon_type, weapon_type=weapon_type, level=level
        ).exists():
            magic_item = cls(
                magic_item_type=magic_weapon_type, weapon_type=weapon_type, level=level
            )
            magic_item.save()


class SimpleMagicItem(ItemAbstract):
    """Base class for simple magic items that only require magic item type and level."""

    class Meta:
        verbose_name = _('Magic item')
        verbose_name_plural = _('Magic items')
        unique_together = ('magic_item_type', 'level')

    SLOT: ClassVar[MagicItemSlot]

    def __str__(self):
        return f'{self.magic_item_type} {self.level} уровня'


class NeckSlotItem(SimpleMagicItem):
    """Magic item for neck slot with defense bonus."""

    class Meta:
        proxy = True

    SLOT = MagicItemSlot.NECK

    @property
    def defence_bonus(self):
        """Get defense bonus equal to enhancement value."""
        return self.enhancement

    def __str__(self):
        return f'{self.magic_item_type}, +{self.enhancement}'


class HeadSlotItem(SimpleMagicItem):
    """Magic item for head slot."""

    class Meta:
        proxy = True

    SLOT = MagicItemSlot.HEAD


class FeetSlotItem(SimpleMagicItem):
    """Magic item for feet slot."""

    class Meta:
        proxy = True

    SLOT = MagicItemSlot.FEET


class ArmsSlotItem(ItemAbstract):
    """Magic item for arms slot that can also function as a shield."""

    class Meta:
        verbose_name = _('Hand item/shield')
        verbose_name_plural = _('Hand items/shields')
        unique_together = ('magic_item_type', 'level', 'shield_type')

    SLOT = MagicItemSlot.ARMS

    shield_type = models.ForeignKey(
        ShieldType,
        verbose_name=_('Shield'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.magic_item_type and not self.shield_type:
            return f'{self.magic_item_type} {self.level} уровня'
        if not self.magic_item_type and self.shield_type:
            return str(self.shield_type)
        return f'{self.magic_item_type} ({self.shield_type}) {self.level} уровня'

    @property
    def skill_penalty(self) -> int:
        """Get skill penalty from shield type if present."""
        if not self.shield_type:
            return 0
        return self.shield_type.skill_penalty


class WaistSlotItem(SimpleMagicItem):
    """Magic item for waist slot."""

    class Meta:
        proxy = True

    SLOT = MagicItemSlot.WAIST


class RingsSlotItem(SimpleMagicItem):
    """Magic item for ring slots."""

    class Meta:
        proxy = True

    SLOT = MagicItemSlot.RING


class HandsSlotItem(SimpleMagicItem):
    """Magic item for hands slot."""

    class Meta:
        proxy = True

    SLOT = MagicItemSlot.HANDS


class NPCMagicItemAbstract(models.Model):
    """Abstract model for NPC equipment slots containing various magic items."""

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
        verbose_name=_('Arms slot/shield'),
        related_name='npc_hands',
    )
