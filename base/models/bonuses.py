from collections import defaultdict
from itertools import chain

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    AbilityEnum,
    BonusSource,
    DefenceTypeEnum,
    NPCOtherProperties,
    PowerFrequencyEnum,
    SkillEnum,
)


class Bonus(models.Model):
    class Meta:
        verbose_name = _('Bonus')
        verbose_name_plural = _('Bonuses')

    name = models.CharField(
        verbose_name=_('Title'), max_length=100, null=True, blank=True
    )
    power = models.ForeignKey(
        "base.Power",
        verbose_name=_('Power'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='bonuses',
        related_query_name='bonus',
        limit_choices_to={'level': 0, 'frequency': PowerFrequencyEnum.PASSIVE.value},
    )
    feat = models.ForeignKey(
        "base.Feat",
        verbose_name=_('Feat'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='bonuses',
        related_query_name='bonus',
    )
    klass = models.ForeignKey(
        'base.Class',
        related_name='bonuses',
        verbose_name=_('Class'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    subclass = models.ForeignKey(
        'base.Subclass',
        verbose_name=_('Subclass'),
        related_name='bonuses',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    functional_template = models.ForeignKey(
        'base.FunctionalTemplate',
        verbose_name=_('Functional template'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='bonuses',
    )
    paragon_path = models.ForeignKey(
        'base.ParagonPath',
        verbose_name=_('Paragon path'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bonuses',
    )
    magic_item_type = models.ForeignKey(
        'MagicItemType',
        verbose_name=_('Magic item type'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bonuses',
    )
    race = models.ForeignKey(
        'base.Race',
        verbose_name=_('Race'),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='bonuses',
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
        choices=chain(
            AbilityEnum.generate_choices(is_sorted=False),
            SkillEnum.generate_choices(is_sorted=False),
            DefenceTypeEnum.generate_choices(is_sorted=False),
            NPCOtherProperties.generate_choices(),
        ),
        max_length=max(
            map(
                lambda x: x.max_length(),
                (
                    AbilityEnum,
                    SkillEnum,
                    DefenceTypeEnum,
                    NPCOtherProperties,
                ),
            )
        ),
        null=True,
        blank=True,
    )
    value = models.CharField(
        verbose_name=_('Value'), null=True, blank=True, max_length=100
    )

    def __str__(self):
        return self.name or ''


class BonusMixin:
    def get_power_bonuses(self) -> models.QuerySet[Bonus]:
        powers_query = models.Q(
            power__in=(
                self.powers.filter(
                    frequency=PowerFrequencyEnum.PASSIVE,
                    subclass__in=(self.subclass_id, 0),
                )
            )
        ) | models.Q(
            power__in=self.race.powers.filter(frequency=PowerFrequencyEnum.PASSIVE)
        )
        if self.functional_template:
            powers_query |= models.Q(
                power__in=self.functional_template.powers.filter(
                    frequency=PowerFrequencyEnum.PASSIVE
                )
            )
        if self.paragon_path:
            powers_query |= models.Q(
                power__in=self.paragon_path.powers.filter(
                    frequency=PowerFrequencyEnum.PASSIVE
                )
            )
        powers_query |= models.Q(power__in=self.magic_item_powers())
        return Bonus.objects.filter(
            (
                powers_query
                | models.Q(feat__id__in=self.feats.all())
                | models.Q(feat__id__in=self.klass.default_feats.all())
                | models.Q(feat__id__in=self.subclass.default_feats.all())
            )
            & models.Q(min_level__lte=self.level)
        )

    def calculate_bonuses(
        self,
        *bonus_types: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties,
    ) -> dict[AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties, int]:
        # TODO refactor query here and in self.get_power_bonuses
        # TODO add cache with refresh on open npc page
        result = {}
        for bonus_type in bonus_types:
            bonuses = defaultdict(list)
            for bonus in (
                self.get_power_bonuses()
                .filter(bonus_type=bonus_type)
                .union(self.race.bonuses.filter(bonus_type=bonus_type))
                .union(self.subclass.bonuses.filter(bonus_type=bonus_type))
                .union(
                    Bonus.objects.filter(
                        magic_item_type__in=(
                            item.magic_item_type for item in self.magic_items
                        )
                    )
                )
            ):
                try:
                    if bonus.feat and not bonus.feat.fits(self):
                        continue
                    item = None
                    if bonus.magic_item_type:
                        # TODO deal with this shitshow
                        for item in self.magic_items:
                            if item.magic_item_type == bonus.magic_item_type:
                                break
                    bonuses[bonus.source].append(
                        int(
                            self.parse_string(
                                accessory_type=None, string=f'${bonus.value}', item=item
                            )
                        )
                    )
                except ValueError:
                    print(f'Bonus processing failed: {bonus}, {bonus.value}')
            result[bonus_type] = sum(max(value) for value in bonuses.values())
        return result

    def calculate_bonus(
        self, bonus_type: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties
    ) -> int:
        return self.calculate_bonuses(bonus_type)[bonus_type]
