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
    """
    Represents a bonus that can be applied to NPC stats from various sources.

    Bonuses can come from races, classes, subclasses, feats, powers, paragon paths,
    functional templates, or magic items. Each bonus has a type (ability, skill,
    defense, or other property) and a value that gets applied to the NPC's stats.
    """

    class Meta:
        verbose_name = _('Bonus')
        verbose_name_plural = _('Bonuses')

    # Optional descriptive name for the bonus
    name = models.CharField(
        verbose_name=_('Title'), max_length=100, null=True, blank=True
    )
    # Link to a passive power that provides this bonus
    # Limited to level 0 passive powers only
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
    # Link to a feat that provides this bonus
    feat = models.ForeignKey(
        "base.Feat",
        verbose_name=_('Feat'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='bonuses',
        related_query_name='bonus',
    )
    # Link to a character class that provides this bonus
    klass = models.ForeignKey(
        'base.Class',
        related_name='bonuses',
        verbose_name=_('Class'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # Link to a character subclass that provides this bonus
    subclass = models.ForeignKey(
        'base.Subclass',
        verbose_name=_('Subclass'),
        related_name='bonuses',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # Link to a functional template that provides this bonus
    # Functional templates modify NPC behavior and stats
    functional_template = models.ForeignKey(
        'base.FunctionalTemplate',
        verbose_name=_('Functional template'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='bonuses',
    )
    # Link to a paragon path that provides this bonus
    # Paragon paths are advanced specializations for high-level characters
    paragon_path = models.ForeignKey(
        'base.ParagonPath',
        verbose_name=_('Paragon path'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bonuses',
    )
    # Link to a magic item type that provides this bonus
    magic_item_type = models.ForeignKey(
        'MagicItemType',
        verbose_name=_('Magic item type'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bonuses',
    )
    # Link to a character race that provides this bonus
    race = models.ForeignKey(
        'base.Race',
        verbose_name=_('Race'),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='bonuses',
    )
    # The source category of this bonus (e.g., racial, enhancement, etc.)
    # Used for bonus stacking rules - bonuses from the same source typically don't stack
    source = models.CharField(
        verbose_name=_('Bonus source'),
        choices=BonusSource.generate_choices(),
        max_length=BonusSource.max_length(),
        null=True,
        blank=True,
    )
    # Minimum character level required to benefit from this bonus
    min_level = models.PositiveSmallIntegerField(
        default=1, verbose_name=_('Minimal level')
    )
    # What type of stat this bonus applies to
    # (ability, skill, defense, or other property)
    # Combines choices from multiple enums to cover all possible bonus targets
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
    # The bonus value - can be a number or formula that gets parsed
    # Examples: "2", "+1", "$lvl/2", "$str"
    value = models.CharField(
        verbose_name=_('Value'), null=True, blank=True, max_length=100
    )

    def __str__(self):
        """Return the bonus name or empty string if no name is set."""
        return self.name or ''


class BonusMixin:
    """
    Mixin class that provides bonus calculation functionality for NPCs.

    This mixin handles finding all applicable bonuses for an NPC based on their
    race, class, subclass, feats, powers, paragon path, functional template,
    and magic items, then calculates the total bonus values with proper stacking rules.
    """

    def get_power_feats_bonuses_query(self: NPCProtocol) -> models.Q:
        """
        Build a Django Q object to find all bonuses from powers and feats
        that apply to this NPC.

        Returns a complex query that includes bonuses from:
        - Passive powers from the NPC's subclass, race,
        functional template, paragon path
        - Powers from magic items
        - Feats directly assigned to the NPC
        - Feats available to the NPC's class or subclass

        Only includes bonuses for which the NPC meets the minimum level requirement.
        """
        # Start with powers from NPC's subclass
        # (including generic subclass_id=0) and race
        powers_query = models.Q(
            power__npcs=self,
            power__subclass__subclass_id__in=(self.subclass_id, 0),
        ) | models.Q(power__race=self.race)

        # Add powers from functional template if NPC has one
        if self.functional_template:
            powers_query |= models.Q(
                power__functional_template=self.functional_template
            )

        # Add powers from paragon path if NPC has one
        if self.paragon_path:
            powers_query |= models.Q(power__paragon_path=self.paragon_path)

        # Restrict to passive powers only (active powers don't provide passive bonuses)
        powers_query = (
            models.Q(power__frequency=PowerFrequencyIntEnum.PASSIVE) & powers_query
        )

        # Also include powers from magic items
        powers_query |= models.Q(power__in=self.magic_item_powers())

        # Combine power bonuses with feat bonuses and apply level restriction
        return (
            powers_query
            | models.Q(feat__npcs=self)  # Feats directly assigned to NPC
            | models.Q(feat__classes=self.klass)  # Feats available to NPC's class
            | models.Q(
                feat__subclasses=self.subclass
            )  # Feats available to NPC's subclass
        ) & models.Q(
            min_level__lte=self.level
        )  # NPC must meet minimum level

    def calculate_bonuses(
        self: NPCProtocol,
        *bonus_types: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties,
        check_cache: bool = False,
    ) -> dict[AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties, int]:
        """
        Calculate total bonus values for the specified bonus types.

        Args:
            *bonus_types: The types of bonuses to calculate
            (abilities, skills, defenses, etc.)
            check_cache: Whether to check cache first for existing calculations

        Returns:
            Dictionary mapping bonus types to their calculated total values

        The method implements D&D 4e bonus stacking rules:
        - Bonuses from the same source don't stack (only highest applies)
        - Bonuses from different sources do stack
        """
        # Check cache first if requested
        if check_cache:
            if result := cache.get(self._bonus_cache_key):
                return {bonus_type: result[bonus_type] for bonus_type in bonus_types}
        result = {}

        # Get all applicable bonuses with optimized database query
        # Use select_related to avoid N+1 queries when accessing related objects
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
            # Could filter by bonus_types here for optimization, but commented out
            # .filter(bonus_type__in=bonus_types)
            .filter(
                # Bonuses from powers and feats (complex query)
                self.get_power_feats_bonuses_query()
                # Direct racial bonuses
                | models.Q(race=self.race)
                # Direct subclass bonuses
                | models.Q(subclass=self.subclass)
                # Bonuses from magic item types this NPC possesses
                | models.Q(
                    magic_item_type__in=(
                        item.magic_item_type for item in self.magic_items
                    )
                )
            ).distinct()
        )
        # Process all possible bonus types
        # (not just requested ones for caching efficiency)
        all_bonus_types = chain(
            AbilityEnum, SkillEnum, DefenceTypeEnum, NPCOtherProperties
        )
        for bonus_type in all_bonus_types:
            # Group bonuses by source to implement stacking rules
            # Key = bonus source, Value = list of bonus values from that source
            bonuses = defaultdict(list)

            # Process each bonus of this type
            for bonus in bonuses_qs.filter(bonus_type=bonus_type):
                try:
                    # Skip feat bonuses if the feat doesn't fit this NPC's requirements
                    if bonus.feat and not bonus.feat.fits(self):
                        continue

                    # Find the specific magic item
                    # if this bonus comes from a magic item type
                    item = None
                    if bonus.magic_item_type:
                        # TODO: This is inefficient - should be refactored
                        # Currently searches through all magic items
                        # to find matching type
                        for item in self.magic_items:
                            if item.magic_item_type == bonus.magic_item_type:
                                break

                    # Parse the bonus value (may contain formulas like "$lvl/2")
                    # Add '$' prefix if not present to indicate it's a formula
                    parsed_value = int(
                        self.parse_string(
                            accessory_type=None, string=f'${bonus.value}', item=item
                        )
                    )

                    # Add to the appropriate source group for stacking calculations
                    bonuses[bonus.source].append(parsed_value)

                except ValueError:
                    # Log parsing errors but continue processing other bonuses
                    print(f'Bonus processing failed: {bonus}, {bonus.value}')
            # Apply D&D 4e stacking rules:
            # - Take the highest bonus from each source
            # - Sum bonuses from different sources
            result[bonus_type] = sum(max(value) for value in bonuses.values())
        # Update cache with new results
        cached_result = cache.get(self._bonus_cache_key, {})
        cached_result.update(result)
        cache.set(self._bonus_cache_key, cached_result)

        # Return only the requested bonus types
        return {bonus_type: cached_result[bonus_type] for bonus_type in bonus_types}

    def calculate_bonus(
        self: NPCProtocol,
        bonus_type: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties,
    ) -> int:
        """
        Calculate the total bonus value for a single bonus type.

        Args:
            bonus_type: The type of bonus to calculate

        Returns:
            The total bonus value for the specified type

        This method checks cache first, then falls back to full calculation if needed.
        """
        # Try to get from cache first
        bonus = cache.get(self._bonus_cache_key)
        if bonus and bonus_type in bonus:
            return bonus[bonus_type]

        # Calculate if not in cache
        return self.calculate_bonuses(bonus_type)[bonus_type]

    def cache_bonuses(self: NPCProtocol):
        """
        Pre-calculate and cache all possible bonus types for this NPC.

        This method calculates bonuses for all abilities, skills, defenses, and other
        properties at once and stores them in cache for faster subsequent access.
        Useful when you know you'll need multiple bonus calculations.
        """
        # Calculate all possible bonus types and store in cache
        cache.set(
            self._bonus_cache_key,
            self.calculate_bonuses(
                *chain(
                    AbilityEnum,  # All character abilities
                    SkillEnum,  # All skills
                    DefenceTypeEnum,  # All defense types
                    NPCOtherProperties,  # All other properties
                )  # type: ignore
            ),
        )

    @property
    def _bonus_cache_key(self: NPCProtocol) -> str:
        """
        Generate a unique cache key for this NPC's bonus calculations.

        Returns:
            A string key that uniquely identifies this NPC's bonus cache entry
        """
        return f'npc-{self.id}-bonuses'
