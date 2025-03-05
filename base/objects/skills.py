from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db.models import QuerySet

if TYPE_CHECKING:
    from base.models.skills import Skill


@dataclass
class Skills:
    acrobatics: int = 0
    arcana: int = 0
    athletics: int = 0
    bluff: int = 0
    diplomacy: int = 0
    dungeoneering: int = 0
    endurance: int = 0
    heal: int = 0
    history: int = 0
    insight: int = 0
    intimidate: int = 0
    nature: int = 0
    perception: int = 0
    religion: int = 0
    stealth: int = 0
    streetwise: int = 0
    thievery: int = 0

    def __add__(self, other):
        return Skills(
            self.acrobatics + other.acrobatics,
            self.arcana + other.arcana,
            self.athletics + other.athletics,
            self.bluff + other.bluff,
            self.diplomacy + other.diplomacy,
            self.dungeoneering + other.dungeoneering,
            self.endurance + other.endurance,
            self.heal + other.heal,
            self.history + other.history,
            self.insight + other.insight,
            self.intimidate + other.intimidate,
            self.nature + other.nature,
            self.perception + other.perception,
            self.religion + other.religion,
            self.stealth + other.stealth,
            self.streetwise + other.streetwise,
            self.thievery + other.thievery,
        )

    def __sub__(self, other):
        return Skills(
            self.acrobatics - other.acrobatics,
            self.arcana - other.arcana,
            self.athletics - other.athletics,
            self.bluff - other.bluff,
            self.diplomacy - other.diplomacy,
            self.dungeoneering - other.dungeoneering,
            self.endurance - other.endurance,
            self.heal - other.heal,
            self.history - other.history,
            self.insight - other.insight,
            self.intimidate - other.intimidate,
            self.nature - other.nature,
            self.perception - other.perception,
            self.religion - other.religion,
            self.stealth - other.stealth,
            self.streetwise - other.streetwise,
            self.thievery - other.thievery,
        )

    @classmethod
    def max(cls, *skills: 'Skills'):
        return Skills(
            acrobatics=max(s.acrobatics for s in skills),
            arcana=max(s.arcana for s in skills),
            athletics=max(s.athletics for s in skills),
            bluff=max(s.bluff for s in skills),
            diplomacy=max(s.diplomacy for s in skills),
            dungeoneering=max(s.dungeoneering for s in skills),
            endurance=max(s.endurance for s in skills),
            heal=max(s.heal for s in skills),
            history=max(s.history for s in skills),
            insight=max(s.insight for s in skills),
            intimidate=max(s.intimidate for s in skills),
            nature=max(s.nature for s in skills),
            perception=max(s.perception for s in skills),
            religion=max(s.religion for s in skills),
            stealth=max(s.stealth for s in skills),
            streetwise=max(s.streetwise for s in skills),
            thievery=max(s.thievery for s in skills),
        )

    @classmethod
    def init_with_const(cls, skills: QuerySet['Skill'], value: int) -> "Skills":
        return Skills(**{skill.name: value for skill in skills})
