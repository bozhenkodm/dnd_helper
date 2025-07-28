from typing import TYPE_CHECKING, cast

from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from base.constants.constants import LEVELS_WITH_ABILITY_BONUS, AbilityEnum
from base.helpers import modifier
from base.models.npc_protocol import NPCProtocol
from base.objects.abilities import Abilities

if TYPE_CHECKING:
    from base.models.models import NPC


class AbilityLevelBonus(models.Model):
    """Tracks ability bonuses gained by NPCs at specific levels.

    Each NPC can receive ability bonuses at certain milestone levels.
    This model represents which ability gets boosted at which level.
    """

    class Meta:
        # Ensure each NPC can only have one bonus per ability per level
        unique_together = ('ability', 'npc', 'level')

    # The ability that receives the bonus
    ability = models.ForeignKey(
        'base.Ability', on_delete=models.CASCADE, related_name='level_bonuses'
    )
    # The NPC receiving the bonus
    npc = models.ForeignKey('base.NPC', on_delete=models.CASCADE)
    # The level at which this bonus is gained
    level = models.PositiveSmallIntegerField(
        choices=((i, i) for i in LEVELS_WITH_ABILITY_BONUS)
    )

    def __str__(self) -> str:
        return f'{self.npc.name} has bonus to {self.ability} on {self.level}'


class Ability(models.Model):
    """Represents the six core D&D abilities: STR, CON, DEX, INT, WIS, CHA."""

    # The ability name (e.g., 'strength', 'dexterity')
    title = models.CharField(
        choices=AbilityEnum.generate_choices(),
        max_length=AbilityEnum.max_length(),
        unique=True,
    )

    def __str__(self) -> str:
        return self.get_title_display()

    @property
    def name(self) -> str:
        """Get lowercase ability name (e.g., 'strength')."""
        return self.title.lower()

    @property
    def short_name(self) -> str:
        """Get 3-letter abbreviation (e.g., 'str')."""
        return self.name[:3]

    @property
    def mod(self) -> str:
        """Get modifier property name (e.g., 'str_mod')."""
        return f'{self.short_name}_mod'


class NPCAbilityAbstract(models.Model):
    """Abstract model providing ability score functionality for NPCs.

    Handles the complex calculation of final ability scores from multiple sources:
    - Base ability scores (set during character creation)
    - Racial bonuses (constant bonuses from race)
    - Variable racial bonus (player choice)
    - Level-based bonuses (gained at milestone levels)
    - Tier bonuses (based on character tier/power level)
    """

    class Meta:
        abstract = True

    # Half the character's level (used in various calculations)
    half_level: int
    # Character's tier (affects all ability scores)
    _tier: int

    # Base ability scores (before any bonuses)
    base_strength = models.SmallIntegerField(verbose_name='Сила (базовая)', default=10)
    base_constitution = models.SmallIntegerField(
        verbose_name='Телосложение (базовое)', default=10
    )
    base_dexterity = models.SmallIntegerField(
        verbose_name='Ловкость (базовая)', default=10
    )
    base_intelligence = models.SmallIntegerField(
        verbose_name='Интеллект (базовый)', default=10
    )
    base_wisdom = models.SmallIntegerField(
        verbose_name='Мудрость (базовая)', default=10
    )
    base_charisma = models.SmallIntegerField(
        verbose_name='Харизма (базовая)', default=10
    )
    # Player's choice for variable racial ability bonus
    var_bonus_ability = models.ForeignKey(
        Ability,
        on_delete=models.SET_NULL,
        verbose_name=_('Selective ability bonus'),
        null=True,
    )
    # Many-to-many relationship tracking level-based ability bonuses
    level_ability_bonuses = models.ManyToManyField(
        Ability,
        blank=True,
        through=AbilityLevelBonus,
        related_name='npcs_for_level_bonuses',
        verbose_name=_('Ability level bonuses'),
    )

    @property
    def _initial_abilities_bonuses(self: NPCProtocol) -> Abilities:
        """Calculate racial ability bonuses (both constant and variable).

        Returns:
            Abilities object with +2 bonuses from race
        """
        # Get constant racial bonuses (e.g., Elves get +2 DEX)
        const_ability_bonus = Abilities.init_with_const(
            self.race.const_ability_bonus.all(),
            value=2,
        )
        # Add player's chosen variable bonus if selected
        if self.var_bonus_ability:
            var_ability_bonus = Abilities.init_with_const(
                Ability.objects.filter(title=self.var_bonus_ability.title), value=2
            )
        else:
            var_ability_bonus = Abilities()
        return const_ability_bonus + var_ability_bonus

    @property
    def _level_abilities_bonuses(self: NPCProtocol) -> Abilities:
        """Calculate bonuses from level-based ability increases.

        Returns:
            Abilities object with bonuses from milestone levels
        """
        # Query to count how many times each ability was boosted
        query = (
            AbilityLevelBonus.objects.select_related('npc', 'ability')
            .filter(npc=cast('NPC', self))
            .values_list(Lower('ability__title'))  # Get ability name
            .annotate(bonus=models.Count('ability__title'))  # Count occurrences
        )
        # Convert query results to dictionary {ability_name: bonus_count}
        bonuses = {item[0]: item[1] for item in query}
        return Abilities(**bonuses)

    @property
    def _tier_attrs_bonus(self: NPCProtocol) -> Abilities:
        """Calculate tier-based bonuses applied to all abilities.

        Higher tier characters get bonuses to all ability scores.

        Returns:
            Abilities object with tier bonus to all abilities
        """
        return Abilities.init_with_const(Ability.objects.all(), value=self._tier)

    @property
    def _base_abilities(self: NPCProtocol) -> Abilities:
        """Get the base ability scores before any bonuses.

        Returns:
            Abilities object with raw base scores
        """
        return Abilities(
            strength=self.base_strength,
            constitution=self.base_constitution,
            dexterity=self.base_dexterity,
            intelligence=self.base_intelligence,
            wisdom=self.base_wisdom,
            charisma=self.base_charisma,
        )

    @property
    def _abilities(self: NPCProtocol) -> Abilities:
        """Calculate final ability scores by combining all bonus sources.

        Returns:
            Abilities object with final calculated ability scores
        """
        return (
            self._initial_abilities_bonuses  # Racial bonuses
            + self._tier_attrs_bonus  # Tier bonuses
            + self._level_abilities_bonuses  # Level milestone bonuses
            + self._base_abilities  # Base scores
        )

    # Final ability score properties (base + all bonuses)
    @property
    def strength(self: NPCProtocol) -> int:
        """Character's final Strength score."""
        return self._abilities.strength

    @property
    def constitution(self: NPCProtocol) -> int:
        """Character's final Constitution score."""
        return self._abilities.constitution

    @property
    def dexterity(self: NPCProtocol) -> int:
        """Character's final Dexterity score."""
        return self._abilities.dexterity

    @property
    def intelligence(self: NPCProtocol) -> int:
        """Character's final Intelligence score."""
        return self._abilities.intelligence

    @property
    def wisdom(self: NPCProtocol) -> int:
        """Character's final Wisdom score."""
        return self._abilities.wisdom

    @property
    def charisma(self: NPCProtocol) -> int:
        """Character's final Charisma score."""
        return self._abilities.charisma

    # Ability modifiers (calculated from ability scores)
    @property
    def str_mod(self: NPCProtocol) -> int:
        """Strength modifier (ability score - 10) / 2."""
        return modifier(self.strength)

    @property
    def con_mod(self: NPCProtocol) -> int:
        """Constitution modifier (ability score - 10) / 2."""
        return modifier(self.constitution)

    @property
    def dex_mod(self: NPCProtocol) -> int:
        """Dexterity modifier (ability score - 10) / 2."""
        return modifier(self.dexterity)

    @property
    def int_mod(self: NPCProtocol) -> int:
        """Intelligence modifier (ability score - 10) / 2."""
        return modifier(self.intelligence)

    @property
    def wis_mod(self: NPCProtocol) -> int:
        """Wisdom modifier (ability score - 10) / 2."""
        return modifier(self.wisdom)

    @property
    def cha_mod(self: NPCProtocol) -> int:
        """Charisma modifier (ability score - 10) / 2."""
        return modifier(self.charisma)

    def get_ability_text(self, ability: Ability) -> str:
        """Format ability score for display with modifier + half level.

        Args:
            ability: The ability to format

        Returns:
            Formatted string like 'STR 16 (+5)' where +5 = modifier + half_level
        """
        # Get the final ability score
        ability_value = getattr(self, ability.name)
        # Get the base modifier
        mod = getattr(self, ability.mod)
        # Format: 'STR 16 (+5)' where +5 includes half-level bonus
        return f'{str(ability)[:3]} ' f'{ability_value} ({mod + self.half_level})'

    @property
    def abilities_texts(self) -> list[str]:
        """Get formatted text for all abilities.

        Returns:
            List of formatted ability strings for display
        """
        return list(self.get_ability_text(ability) for ability in Ability.objects.all())
