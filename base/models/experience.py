from typing import Protocol

from django.db import models
from django.utils.translation import gettext_lazy as _

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
    level: int
    experience: int


class NPCExperienceAbstract(models.Model):
    class Meta:
        abstract = True

    experience = models.IntegerField(verbose_name=_('Experience'), default=0)

    @staticmethod
    def level_by_experience(experience) -> int:
        level = 1
        for level, exp in enumerate(EXPERIENCE_BY_LEVEL, start=1):
            if experience == exp:
                return level
            if experience < exp:
                return level - 1
        return level

    @staticmethod
    def experience_by_level(level: int) -> int:
        return EXPERIENCE_BY_LEVEL[level - 1]
