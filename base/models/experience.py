from typing import Protocol

from django.db import models
from django.utils.translation import gettext_lazy as _

# Experience points required for each character level (1-30)
# Index 0 = Level 1 (0 XP), Index 1 = Level 2 (1000 XP), etc.
EXPERIENCE_BY_LEVEL = [
    0,
    1000,
    2250,
    3750,
    5500,
    7500,
    10000,
    13000,
    16500,
    20500,
    26000,
    32000,
    39000,
    47000,
    57000,
    69000,
    83000,
    99000,
    119000,
    143000,
    175000,
    210000,
    255000,
    310000,
    375000,
    450000,
    550000,
    675000,
    825000,
    1000000,
]


class NPCProtocol(Protocol):
    """Protocol defining the interface for NPC objects
    that have level and experience.
    """

    level: int
    experience: int


class NPCExperienceAbstract(models.Model):
    """Abstract model providing experience-related functionality for NPCs."""

    class Meta:
        abstract = True

    # Character's current experience points
    experience = models.IntegerField(verbose_name=_('Experience'), default=0)

    @staticmethod
    def level_by_experience(experience) -> int:
        """Calculate character level based on experience points.

        Args:
            experience: Total experience points

        Returns:
            Character level (1-30)
        """
        level = 1
        # Iterate through experience thresholds to find appropriate level
        for level, exp in enumerate(EXPERIENCE_BY_LEVEL, start=1):
            # Exact match - return this level
            if experience == exp:
                return level
            # Experience is less than threshold - return previous level
            if experience < exp:
                return level - 1
        # Experience exceeds all thresholds - return max level
        return level

    @staticmethod
    def experience_by_level(level: int) -> int:
        """Get minimum experience points required for a given level.

        Args:
            level: Character level (1-30)

        Returns:
            Minimum experience points required for that level
        """
        # Convert level to array index (level 1 = index 0)
        return EXPERIENCE_BY_LEVEL[level - 1]
