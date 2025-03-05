from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from base.constants.constants import (
    ArmorTypeIntEnum,
    NPCRaceEnum,
    PowerFrequencyIntEnum,
    ShieldTypeIntEnum,
    WeaponHandednessEnum,
)
from base.models.abstract import ConstraintAbstract
from base.models.books import BookSource
from base.models.items import WeaponCategory, WeaponGroup
from base.objects.powers_output import PowerDisplay


class Feat(ConstraintAbstract):
    class Meta:
        verbose_name = _('Feat')
        verbose_name_plural = _('Feats')

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    min_level = models.PositiveSmallIntegerField(
        verbose_name=_('Minimal level'), default=1, choices=((1, 1), (11, 11), (21, 21))
    )
    text = models.TextField(verbose_name=_('Text'), null=True, blank=True)
    book_source = models.ForeignKey(
        BookSource,
        verbose_name=_('Source'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        constraints = []
        conditions = []
        name = (
            self.name
            if self.min_level == 1
            else f'{self.name}, {self.min_level} уровень'
        )
        for constraint in self.constraints.all():
            if constraint.conditions.all():
                conditions.append(
                    ', '.join(
                        f'{condition.content_type}: {condition.condition}'
                        for condition in constraint.conditions.all()
                    )
                )
            if constraint.scalar_conditions.all():
                conditions.append(
                    ', '.join(
                        f'{condition.get_type_display()}: {condition.value_display}'
                        for condition in constraint.scalar_conditions.all()
                    )
                )
            # TODO add availability_conditions
            constraints.append(', '.join(conditions))
        if not constraints:
            return f'{name}. {self.text}'
        return f'{name}. {_(" or ").join(constraints)}. {self.text}'

    def fits(self, npc) -> bool:
        for item_state in self.item_states.all():
            if item_state.shield and str(npc.shield) not in item_state.shield:
                return False
            if (
                item_state.armor
                and str(npc.armor.armor_type.base_armor_type) not in item_state.armor
            ):
                return False
            if not item_state.primary_hand_fits(npc):
                return False
            if not item_state.secondary_hand_fits(npc):
                return False
        return True


class WeaponState(models.Model):
    is_empty = models.BooleanField(_('Is hand empty?'), default=False, blank=True)
    handedness = MultiSelectField(
        choices=WeaponHandednessEnum.generate_choices(is_sorted=False),
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField(
        WeaponCategory, verbose_name=_('Weapon category'), blank=True
    )
    groups = models.ManyToManyField(
        WeaponGroup,
        verbose_name=_('Weapon groups'),
        blank=True,
    )
    type = models.ManyToManyField(
        'base.WeaponType',
        verbose_name=_('Weapon type'),
        blank=True,
        related_name='primary_hand_conditions',
    )

    def __str__(self):
        if self.is_empty:
            return 'Рука должна быть пустая'
        result = []
        if self.categories.all():
            result.append(
                'Категория: '
                + ', '.join(c.get_code_display() for c in self.categories.all())
            )
        if self.groups.all():
            result.append(
                'Группа: '
                + ', '.join(wg.get_name_display() for wg in self.groups.all())
            )
        if self.type.all():
            result.append('Тип: ' + ', '.join(str(wt) for wt in self.type.all()))
        if not any((self.categories.all(), self.groups.all(), self.type.all())):
            return 'Рука должна быть не пустая'
        return '; '.join(result)


class ItemState(models.Model):
    feat = models.ForeignKey(Feat, on_delete=models.CASCADE, related_name='item_states')
    primary_hand = models.ForeignKey(
        WeaponState,
        verbose_name=_('Primary hand'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_hands',
    )
    secondary_hand = models.ForeignKey(
        WeaponState,
        verbose_name=_('Secondary hand'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secondary_hands',
    )
    shield = MultiSelectField(
        verbose_name=_('Shield type'),
        choices=ShieldTypeIntEnum.generate_choices(),
        null=True,
        blank=True,
    )
    armor = MultiSelectField(
        verbose_name=_('Armor type'),
        choices=ArmorTypeIntEnum.generate_choices(),
        null=True,
        blank=True,
    )

    def primary_hand_fits(self, npc) -> bool:
        if not self.primary_hand:
            return True
        if self.primary_hand.is_empty == bool(npc.primary_hand):
            return False
        if (
            self.primary_hand.categories.all()
            and npc.primary_hand.category not in self.primary_hand.categories.all()
        ):
            return False
        if (
            self.primary_hand
            and self.primary_hand.groups.all()
            and not npc.primary_hand.groups().exclude(
                id__in=self.primary_hand.groups.values_list('id', flat=True)
            )
        ):
            return False
        if (
            self.primary_hand.type.all()
            and npc.primary_hand.weapon_type not in self.primary_hand.type.all()
        ):
            return False
        return True

    def secondary_hand_fits(self, npc) -> bool:
        secondary_hand = npc.secondary_hand or (
            npc.primary_hand.secondary_end
            if hasattr(npc.primary_hand, 'secondary_end')
            else None
        )
        if not self.secondary_hand:
            return True
        if self.secondary_hand.is_empty == bool(secondary_hand):
            return False
        if (
            self.secondary_hand.categories.all()
            and secondary_hand.category not in self.secondary_hand.categories.all()
        ):
            return False
        if (
            self.secondary_hand
            and self.secondary_hand.groups.all()
            and not npc.secondary_hand.groups().exclude(
                id__in=self.secondary_hand.groups.values_list('id', flat=True)
            )
        ):
            return False
        if (
            self.secondary_hand.type.all()
            and secondary_hand.weapon_type not in self.secondary_hand.type.all()
        ):
            return False
        return True


class NPCFeatAbstract(models.Model):
    class Meta:
        abstract = True

    feats = models.ManyToManyField(Feat, blank=True, verbose_name=_('Feats'))
    trained_weapons = models.ManyToManyField(
        'base.WeaponType',
        blank=True,
        verbose_name=_('Trained weapon'),
        help_text=_('Weapon training in addition to training by race and class'),
    )

    @property
    def feats_count(self) -> int:
        return self.feats.count() + self.trained_weapons.count()

    @property
    def max_feats_number(self) -> int:
        result = self.half_level + self._tier + 1
        if self.race.name == NPCRaceEnum.HUMAN:
            result += 1
        return result

    def feats_calculated(self):
        not_empty_text_query = models.Q(text__isnull=False) & ~models.Q(text='')
        feats_qs = (
            self.klass.default_feats.filter(not_empty_text_query)
            | self.subclass.default_feats.filter(not_empty_text_query)
            | self.feats.filter(not_empty_text_query)
        )
        feats: list[dict] = []
        for feat in feats_qs:
            if not feat.fits(self):
                continue
            feats.append(
                PowerDisplay(
                    name=feat.name,
                    keywords='',
                    category='Черта',
                    description=self.parse_string(
                        accessory_type=None, string=feat.text
                    ),
                    frequency_order=-1,
                    frequency_css_class=PowerFrequencyIntEnum.PASSIVE.name.lower(),
                    frequency='',
                    properties=[],
                ).asdict()
            )
        return feats
