from collections import defaultdict
from itertools import chain

from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import (
    AbilityEnum,
    BonusSource,
    DefenceTypeEnum,
    NPCOtherProperties,
    PowerFrequencyIntEnum,
    SkillEnum,
)
from base.models.npc_protocol import NPCProtocol


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
        limit_choices_to={'level': 0, 'frequency': PowerFrequencyIntEnum.PASSIVE.value},
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
    def get_power_feats_bonuses_query(self: NPCProtocol) -> models.Q:
        powers_query = models.Q(
            power__npcs=self,
            power__subclass__subclass_id__in=(self.subclass_id, 0),
        ) | models.Q(power__race=self.race)
        if self.functional_template:
            powers_query |= models.Q(
                power__functional_template=self.functional_template
            )
        if self.paragon_path:
            powers_query |= models.Q(power__paragon_path=self.paragon_path)
        powers_query = (
            models.Q(power__frequency=PowerFrequencyIntEnum.PASSIVE) & powers_query
        )
        powers_query |= models.Q(power__in=self.magic_item_powers())
        return (
            powers_query
            | models.Q(feat__npcs=self)
            | models.Q(feat__classes=self.klass)
            | models.Q(feat__subclasses=self.subclass)
        ) & models.Q(min_level__lte=self.level)

    def calculate_bonuses(
        self: NPCProtocol,
        *bonus_types: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties,
        check_cache: bool = False,
    ) -> dict[AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties, int]:
        if check_cache:
            if result := cache.get(self._bonus_cache_key):
                return {bonus_type: result[bonus_type] for bonus_type in bonus_types}
        result = {}
        bonuses_qs = (
            Bonus.objects.select_related(
                'race',
                'subclass',
                'magic_item_type',
                'functional_template',
                'paragon_path',
                'power',
                'feat',
            )
            # .filter(bonus_type__in=bonus_types)
            .filter(
                self.get_power_feats_bonuses_query()
                | models.Q(race=self.race)
                | models.Q(subclass=self.subclass)
                | models.Q(
                    magic_item_type__in=(
                        item.magic_item_type for item in self.magic_items
                    )
                )
            ).distinct()
        )
        bonus_types = chain(AbilityEnum, SkillEnum, DefenceTypeEnum, NPCOtherProperties)
        for bonus_type in bonus_types:
            bonuses = defaultdict(list)
            for bonus in bonuses_qs.filter(bonus_type=bonus_type):
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
        cached_result = cache.get(self._bonus_cache_key, {})
        cached_result.update(result)
        cache.set(self._bonus_cache_key, cached_result)
        return cached_result

    def calculate_bonus(
        self: NPCProtocol,
        bonus_type: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties,
    ) -> int:
        bonus = cache.get(self._bonus_cache_key)
        if bonus and bonus_type in bonus:
            return bonus[bonus_type]
        return self.calculate_bonuses(bonus_type)[bonus_type]

    def cache_bonuses(self: NPCProtocol):
        cache.set(
            self._bonus_cache_key,
            self.calculate_bonuses(
                *chain(AbilityEnum, SkillEnum, DefenceTypeEnum, NPCOtherProperties)
            ),
        )

    @property
    def _bonus_cache_key(self: NPCProtocol) -> str:
        return f'npc-{self.id}-bonuses'
